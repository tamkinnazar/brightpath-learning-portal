from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory user list for demo/testing.
# Later this can be replaced with PostgreSQL / Cloud SQL.
users = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        users.append({
            "username": username,
            "password": password,
            "role": role
        })

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        for user in users:
            if user["username"] == username and user["password"] == password:
                return redirect(url_for("dashboard"))

        message = "Invalid username or password."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/courses")
def courses():
    courses_list = [
        "Cybersecurity Fundamentals",
        "Network Security",
        "Cloud Security",
        "Digital Forensics"
    ]
    return render_template("courses.html", courses=courses_list)


@app.route("/assignments")
def assignments():
    assignments_list = [
        "Week 9 Security Audit",
        "Week 10 Backend Implementation",
        "Week 11 Final Capstone Submission"
    ]
    return render_template("assignments.html", assignments=assignments_list)


@app.route("/grades")
def grades():
    grades_list = [
        {"course": "Cybersecurity Fundamentals", "grade": "A"},
        {"course": "Network Security", "grade": "B+"},
        {"course": "Cloud Security", "grade": "A-"}
    ]
    return render_template("grades.html", grades=grades_list)


if __name__ == "__main__":
    app.run(debug=True)
