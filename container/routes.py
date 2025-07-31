from container import app
from flask import render_template, redirect, url_for, flash
from container.models import User, Skill, Progress
from container.forms import RegisterForm, LoginForm, AddSkillForm, LogProgressForm
from container import db
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/dashboard")
@login_required
def dashboard_page():
    # Get all skills for the current user with their progress
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', skills=skills)





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

        if attempted_user and attempted_user.check_password_correction(
            form.password.data):
            login_user(attempted_user)
            flash(f"You have successfully logged in as {attempted_user.username}", category = 'success')
            return redirect(url_for('dashboard_page'))
        
        else:
            flash(f"Username and password don't match! Try again!", category = 'danger')

    return render_template('login.html', form = form)




@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category = 'info')
    
    return redirect(url_for('home_page'))




@app.route('/add-skill', methods = ['GET', 'POST'])
@login_required
def add_skill_page():
    form = AddSkillForm()

    if form.validate_on_submit():
        existing_skill = Skill.query.filter_by(name=form.name.data,
                user_id=current_user.id).first()
        
        if existing_skill:
            flash(f"You already have skill named '{form.name.data}'!", category = 'danger')
            return render_template('add_skill.html',form=form)


        skill_to_create = Skill(name=form.name.data,
                            description=form.description.data,
                            category=form.category.data,
                            target_hours=form.target_hours.data,
                            user_id=current_user.id)
        
        db.session.add(skill_to_create)
        db.session.commit()
    
        flash(f"Skill {skill_to_create.name} added successfully!", category = 'success')
        return redirect(url_for('dashboard_page'))  
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error adding skill: {err_msg}", category = 'danger')
    
    return render_template('add_skill.html', form=form)





@app.route('/log-progress', methods = ['GET', 'POST'])
@login_required
def log_progress_page():
    form = LogProgressForm()

    user_skills = Skill.query.filter_by(user_id = current_user.id).all()
    form.skill_id.choices = [(skill.id, skill.name) for skill in user_skills]

    if not user_skills:
        flash("You need to add some skills before logging progress!", category = 'info')
        return redirect(url_for('add_skill_page'))
    
    if form.validate_on_submit():
        today = datetime.now().date()

        existing_progress = Progress.query.filter_by(
            skill_id = form.skill_id.data, date = today).first()
        
        if existing_progress:
            flash("Progress already logged for this skill today! You can log once per day per skill!", category = 'danger')
            return render_template('log_progress.html', form = form)

        
        progress_to_create = Progress(skill_id = form.skill_id.data,
                        hours_spent = form.hours_spent.data,
                        notes = form.notes.data,
                        difficulty_rating = form.difficulty_rating.data)
        
        db.session.add(progress_to_create)
        db.session.commit()
    
        skill = Skill.query.get(form.skill_id.data)
        flash(f"Progress logged for '{skill.name}' - {form.hours_spent.data} hours!", category='success')
        return redirect(url_for('dashboard_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error logging progress: {err_msg}", category='danger')

    return render_template('log_progress.html', form=form)







@app.route("/delete-skill/<int:skill_id>", methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if the skill belongs to the current user
    if skill.user_id != current_user.id:
        flash("You can only delete your own skills!", category='danger')
        return redirect(url_for('dashboard_page'))
    
    skill_name = skill.name
    db.session.delete(skill)
    db.session.commit()
    
    flash(f"Skill '{skill_name}' and all its progress entries have been deleted!", category='success')
    return redirect(url_for('dashboard_page'))






@app.route('/charts')
def charts_page():
    return render_template('charts.html')





















