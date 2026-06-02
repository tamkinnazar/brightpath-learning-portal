from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route("/grades")
def grades():
    return render_template("grades.html")

if __name__ == "__main__":
    app.run(debug=True)
