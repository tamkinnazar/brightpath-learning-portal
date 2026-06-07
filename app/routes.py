from flask import Blueprint, render_template, request, redirect, session, url_for
from app.db import get_db_connection
import bcrypt
import os
from werkzeug.utils import secure_filename
from google.cloud import storage
from pymysql.err import IntegrityError

main = Blueprint("main", __name__)

# -------------------------
# HOME
# -------------------------
@main.route("/")
def home():
    if "user" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


# -------------------------
# SIGNUP / REGISTER
# -------------------------
# SIGNUP / REGISTER (CHANGED ROUTE PATH TO FIX 404)
# -------------------------
@main.route("/signup", methods=["GET", "POST"])  # <-- Changed from "/register" to "/signup"
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Username and password are required.", 400

        try:
            # Hash password securely using bcrypt
            password_bytes = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO students (username, password, image_url) VALUES (%s, %s, NULL)",
                        (username, hashed_password)
                    )
                    conn.commit()
            
            return redirect(url_for("main.login"))

        except IntegrityError:
            return "Username already exists. Please pick a different one.", 409
        except Exception as e:
            print(f"Registration error: {e}", flush=True)
            return "An error occurred during account creation.", 500

    return render_template("signup.html")

# -------------------------
# LOGIN (FULLY FUNCTIONAL & DICT-SAFE)
# -------------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Username and password are required.", 400

        user = None
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Removed the hardcoded "USE brightpath_db;" line
                cursor.execute("SELECT username, password FROM students WHERE username = %s", (username,))
                user = cursor.fetchone()
                
        if user:
            if isinstance(user, dict):
                db_username = user.get('username')
                db_hashed_password = user.get('password')
            else:
                db_username = user[0]
                db_hashed_password = user[1]

            if db_hashed_password:
                db_hashed_password = str(db_hashed_password).strip()

            try:
                password_bytes = password.encode('utf-8')
                hash_bytes = db_hashed_password.encode('utf-8')

                if bcrypt.checkpw(password_bytes, hash_bytes):
                    session["user"] = db_username
                    return redirect(url_for('main.dashboard'))
                else:
                    return "Incorrect password. Please go back and try again.", 401
            except Exception as e:
                print(f"Bcrypt error encountered: {e}", flush=True)
                return "An internal authentication error occurred.", 500
        else:
            return "Username does not exist. Please check your spelling or sign up.", 404

    return render_template("login.html")



# PROFILE UPLOAD (BULLETPROOF AGNOSTIC EXTRACTOR)
# -------------------------
@main.route("/upload-profile", methods=["POST"])
def upload_profile():
    if "user" not in session:
        return redirect(url_for("main.login"))

    # FIX: Grab the FIRST available file payload found in the request, ignoring key names entirely
    file = None
    if request.files:
        first_key = list(request.files.keys())[0]
        file = request.files[first_key]

    # Extreme safety fallback check
    if not file or file.filename == "":
        return "No file uploaded or missing file input field in form. Please verify form headers.", 400

    filename = secure_filename(file.filename)
    bucket_name = os.getenv("BUCKET_NAME")

    if not bucket_name:
        print("CRITICAL: BUCKET_NAME environment variable is missing!", flush=True)
        return "Server configuration error: Upload bucket missing.", 500

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(filename)

        # Secure chunking allocations
        blob.chunk_size = 256 * 1024  
        file.seek(0)
        blob.upload_from_file(file, content_type=file.content_type)

        image_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET image_url=%s WHERE username=%s",
                    (image_url, session["user"])
                )
                conn.commit()

    except Exception as e:
        print(f"File upload execution failed due to an error: {e}", flush=True)
        return "An internal server error occurred during file processing.", 500

    # FIX: Notice there are exactly 4 spaces here! It is inside the function base layer.
    return redirect(url_for("main.dashboard"))

# -------------------------
# DASHBOARD
# -------------------------
# -------------------------
# DASHBOARD
# -------------------------
@main.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("main.login"))

    username = session["user"]
    image_url = None

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Query the profile link out for the current user
                cursor.execute("SELECT image_url FROM students WHERE username = %s", (username,))
                result = cursor.fetchone()

                # PyMySQL safety parsing block:
                if result:
                    if isinstance(result, dict):
                        image_url = result.get("image_url")
                    elif isinstance(result, (tuple, list)) and len(result) > 0:
                        image_url = result[0]

    except Exception as e:
        print(f"Database read error on dashboard load: {e}", flush=True)
        image_url = None 

    # If it's empty string or null, default it out back to None
    if not image_url or str(image_url).strip() == "" or str(image_url) == "None":
        image_url = None

    # Crucial mapping step: passing the database value to 'photo' variable
    return render_template("dashboard.html", user=username, photo=image_url)
# -------------------------
# LOGOUT
# -------------------------
@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# -------------------------
# COURSES
# -------------------------
@main.route("/courses")
def courses():
    if "user" not in session:
        return redirect(url_for("main.login"))

    return render_template("courses.html")


# -------------------------
# ASSIGNMENTS
# -------------------------
@main.route("/assignments")
def assignments():
    if "user" not in session:
        return redirect(url_for("main.login"))

    return render_template("assignments.html")


# -------------------------
# PROGRESS
# -------------------------
# -------------------------
# PROGRESS ROUTE (FORCED UPDATED)
# -------------------------
@main.route("/progress")
def progress():
    if "user" not in session:
        return redirect(url_for("main.login"))

    # Explicitly return 95% down into the template view
    return render_template("progress.html", user=session["user"], progress=95, completed=19, total=20)
