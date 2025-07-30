from container import app
from flask import render_template, redirect, url_for, flash, request
from container.models import User
from container.forms import RegisterForm, LoginForm
from container import db
from flask_login import login_user, logout_user, login_required, current_user


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

    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                            email_address = form.email_address.data,
                            password = form.password1.data
                            )
        
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category = 'success')
        
        return redirect(url_for('dashboard_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error creating a user: {err_msg}", category = 'danger')

    return render_template('register.html', form = form)





@app.route("/login", methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()

        # if attempted_user and 



    return render_template('login.html', form = form)


