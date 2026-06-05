from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import bcrypt
from werkzeug.utils import secure_filename
from google.cloud import storage
from app.db import get_db_connection

main = Blueprint('main', __name__)

# -------------------------
# DB
# -------------------------
def get_db():
    return get_db_connection()

# -------------------------
# GCS UPLOAD
# -------------------------
def upload_to_gcs(file):
    bucket_name = os.getenv("BUCKET_NAME")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    filename = secure_filename(file.filename)
    blob = bucket.blob(filename)

    blob.upload_from_file(file)
    blob.make_public()

    return blob.public_url

# -------------------------
# LOGIN
# -------------------------
@main.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM students WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            session['user'] = username
            session['photo'] = user.get('image_url')
            return redirect(url_for('main.dashboard'))

        error = "Invalid username or password ❌"

    return render_template('login.html', error=error)

# -------------------------
# SIGNUP
# -------------------------
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match ❌"

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO students (username, password) VALUES (%s, %s)",
            (username, hashed.decode())
        )

        db.commit()
        return redirect(url_for('main.login'))

    return render_template('signup.html')

# -------------------------
# DASHBOARD
# -------------------------
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template(
        'dashboard.html',
        user=session['user'],
        photo=session.get('photo')
    )

# -------------------------
# ASSIGNMENTS (FIXED)
# -------------------------
@main.route('/assignments')
def assignments():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('assignments.html')

# -------------------------
# COURSES (FIXED)
# -------------------------
@main.route('/courses')
def courses():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('courses.html')

# -------------------------
# PROGRESS (FIXED)
# -------------------------
@main.route('/progress')
def progress():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return "<h1>Progress Page Coming Soon</h1>"

# -------------------------
# PROFILE UPLOAD
# -------------------------
@main.route('/upload-profile', methods=['POST'])
def upload_profile():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    file = request.files.get('profile_pic')

    if not file or file.filename == '':
        return "No file selected", 400

    url = upload_to_gcs(file)

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE students SET image_url=%s WHERE username=%s",
        (url, session['user'])
    )

    db.commit()

    session['photo'] = url

    return redirect(url_for('main.dashboard'))

# -------------------------
# LOGOUT
# -------------------------
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))