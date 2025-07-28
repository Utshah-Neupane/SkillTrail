from container import app
from flask import render_template


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/dashboard")
def dashboard_page():
    return render_template('dashboard.html')


@app.route("/login")
def login_page():
    return render_template('login.html')


@app.route("/register")
def register_page():
    return render_template('register.html')
