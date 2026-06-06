from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import mysql.connector
import bcrypt
from werkzeug.utils import secure_filename
from google.cloud import storage

main = Blueprint('main', __name__)

# =========================
# DB CONNECTION (CLOUD RUN SAFE)
# =========================
def get_db():
    return mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        unix_socket=f"/cloudsql/{os.getenv('DB_CONNECTION_NAME')}"
    )

# =========================
# LOGIN
# =========================
@main.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            session['user'] = username
            return redirect(url_for('main.dashboard'))

        error = "Invalid login"

    return render_template('login.html', error=error)

# =========================
# SIGNUP
# =========================
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

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

# =========================
# DASHBOARD
# =========================
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('dashboard.html', user=session['user'])

# =========================
# LOGOUT (ONLY ONCE)
# =========================
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

# =========================
# COURSES (ONLY ONCE)
# =========================
@main.route('/courses')
def courses():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('courses.html', user=session['user'])

# =========================
# ASSIGNMENTS (ONLY ONCE)
# =========================
@main.route('/assignments')
def assignments():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    return render_template('assignments.html', user=session['user'])

# =========================
# PROFILE UPLOAD
# =========================
@main.route('/upload-profile', methods=['POST'])
def upload_profile():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    if 'profile_pic' not in request.files:
        return "No file uploaded", 400

    file = request.files['profile_pic']

    bucket_name = os.getenv("BUCKET_NAME")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    filename = secure_filename(file.filename)
    blob = bucket.blob(filename)

    blob.upload_from_file(file)
    blob.make_public()

    url = blob.public_url

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE students SET image_url=%s WHERE username=%s",
        (url, session['user'])
    )
    db.commit()

    return redirect(url_for('main.dashboard'))