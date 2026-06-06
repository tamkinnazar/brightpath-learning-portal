from flask import Blueprint, render_template, request, redirect, session, url_for
from app.db import get_db_connection
import bcrypt
import os
from werkzeug.utils import secure_filename
from google.cloud import storage

main = Blueprint("main", __name__)

# -------------------------
# HOME
# -------------------------
@main.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


# -------------------------
# SIGNUP
# -------------------------
@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (username, password) VALUES (%s, %s)",
            (username, hashed)
        )

        return redirect("/login")

    return render_template("signup.html")


# -------------------------
# LOGIN
# -------------------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE username=%s", (username,))
        user = cursor.fetchone()

        # ✅ SAFE CHECK (prevents crash)
        if not user:
            return "Invalid credentials"

        stored_password = user["password"]

        # convert safely to bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            session["user"] = username
            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


# -------------------------
# DASHBOARD
# -------------------------
@main.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])


# -------------------------
# LOGOUT
# -------------------------
@main.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------------------------
# PROFILE UPLOAD (GCS FIXED)
# -------------------------
@main.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect("/login")

    file = request.files.get("image") or request.files.get("file")

    if not file or file.filename == "":
        return "No file uploaded", 400

    filename = secure_filename(file.filename)

    bucket_name = os.getenv("BUCKET_NAME")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_file(file, content_type=file.content_type)

    image_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET image_url=%s WHERE username=%s",
        (image_url, session["user"])
    )

    return redirect("/dashboard")


# -------------------------
# COURSES (FIX FOR NOT FOUND)
# -------------------------
@main.route("/courses")
def courses():
    if "user" not in session:
        return redirect("/login")

    return render_template("courses.html")


# -------------------------
# ASSIGNMENTS (FIX FOR NOT FOUND)
# -------------------------
@main.route("/assignments")
def assignments():
    if "user" not in session:
        return redirect("/login")

    return render_template("assignments.html")