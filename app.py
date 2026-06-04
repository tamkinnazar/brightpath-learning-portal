import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "replace-this-secret-key-before-production"

DATABASE = "brightpath.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            course_title TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')

    if conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO courses (title, description) VALUES (?, ?)",
            [
                ("Cybersecurity Fundamentals", "Introduction to cybersecurity concepts and best practices."),
                ("Network Security", "Covers firewalls, secure networks, and monitoring."),
                ("Cloud Security", "Focuses on securing cloud applications and infrastructure."),
                ("Digital Forensics", "Introduces investigation and evidence handling techniques.")
            ]
        )

    if conn.execute("SELECT COUNT(*) FROM assignments").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO assignments (course_id, title, description) VALUES (?, ?, ?)",
            [
                (1, "Week 9 Security Audit", "Complete a basic security audit report."),
                (2, "Week 10 Backend Implementation", "Build and test backend application routes."),
                (3, "Week 11 Final Capstone Submission", "Prepare final project documentation and demo.")
            ]
        )

    if conn.execute("SELECT COUNT(*) FROM grades").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO grades (student_name, course_title, grade) VALUES (?, ?, ?)",
            [
                ("Student Demo", "Cybersecurity Fundamentals", "A"),
                ("Student Demo", "Network Security", "B+"),
                ("Student Demo", "Cloud Security", "A-")
            ]
        )

    conn.commit()
    conn.close()


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


def role_required(*allowed_roles):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if "role" not in session:
                flash("Please log in first.")
                return redirect(url_for("login"))

            if session["role"] not in allowed_roles:
                flash("You do not have permission to access that page.")
                return redirect(url_for("dashboard"))

            return view_function(*args, **kwargs)
        return wrapped_view
    return decorator


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            flash("Account created successfully. Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another username.")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash("Logged in successfully.")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/courses")
@login_required
def courses():
    conn = get_db_connection()
    courses_data = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses_data)


@app.route("/assignments")
@login_required
def assignments():
    conn = get_db_connection()
    assignments_data = conn.execute('''
        SELECT assignments.id, assignments.title, assignments.description, courses.title AS course_title
        FROM assignments
        LEFT JOIN courses ON assignments.course_id = courses.id
    ''').fetchall()
    conn.close()
    return render_template("assignments.html", assignments=assignments_data)


@app.route("/grades")
@login_required
def grades():
    conn = get_db_connection()
    grades_data = conn.execute("SELECT * FROM grades").fetchall()
    conn.close()
    return render_template("grades.html", grades=grades_data)


@app.route("/admin")
@login_required
@role_required("administrator")
def admin():
    conn = get_db_connection()
    users_data = conn.execute("SELECT id, username, role FROM users").fetchall()
    conn.close()
    return render_template("admin.html", users=users_data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
