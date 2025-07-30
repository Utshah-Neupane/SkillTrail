from container import app
from flask import render_template
from container.forms import RegisterForm, LoginForm


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/dashboard")
def dashboard_page():
    return render_template('dashboard.html')



@app.route("/register", methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    return render_template('register.html', form = form)



@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form = form)


