from container import app
from flask import render_template, redirect, url_for, flash, make_response
from container.models import User, Skill, Progress
from container.forms import RegisterForm, LoginForm, AddSkillForm, LogProgressForm
from container import db
from flask_login import login_required, login_user, logout_user, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd

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
@login_required
def charts_page():
    user_skills = Skill.query.filter_by(user_id = current_user.id).all()

    if not user_skills:
        flash('Add some skills to see progress!', category='warning')
        return redirect(url_for('add_skill_page'))


    #Chart 1: Progress Overview
    progress_categories = {'Beginner (0-49%)': 0, 'Intermediate (50-74%)': 0, 
                    'Advanced (75-99%)': 0, 'Completed (100%)': 0}

    for skill in user_skills:
        percentage = skill.progress_percentage
        if percentage == 100:
            progress_categories['Completed (100%)'] += 1
        elif percentage >= 75:
            progress_categories['Advanced (75-99%)'] += 1
        elif percentage >= 50:
            progress_categories['Intermediate (50-74%)'] += 1
        else:
            progress_categories['Beginner (0-49%)'] += 1
    


    # Chart 2: Learning Trends
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=29)

    # Fixed query syntax
    daily_progress = db.session.query(
        Progress.date,
        func.sum(Progress.hours_spent).label('hours_spent')
        ).join(Skill).filter(
            Skill.user_id == current_user.id,
            Progress.date >= start_date,
            Progress.date <= end_date
        ).group_by(Progress.date).order_by(Progress.date).all()
    
    date_range = []
    hours_data = []
    current_date = start_date
    progress_dict = {entry.date: float(entry.hours_spent) for entry in daily_progress}

    while current_date <= end_date:
        date_range.append(current_date.strftime('%m:%d'))
        hours_data.append(progress_dict.get(current_date,0))
        current_date += timedelta(days = 1)


    
    #Chart 3: Category Breakdown (Hours spent per skill category)
    category_dict = {}

    for skill in user_skills:
        category_name = skill.category or "Uncategorized"
        category_dict[category_name] = skill.total_hours_logged + category_dict.get(category_name, 0)


    charts_data = {
        'progress_overview':{
            'labels' : list(progress_categories.keys()),
            'data' : list(progress_categories.values())
        },

        'learning_trends': {
            'labels': date_range,
            'data': hours_data
        },

        'category_breakdown':{
            'labels' : list(category_dict.keys()),
            'data': list(category_dict.values())
        }
    }
    

    return render_template('charts.html', charts_data = charts_data)







@app.route('/reports')
@login_required
def reports_page():
    # Check if user has premium access
    if not current_user.is_premium:
        flash("Upgrade to Premium to access advanced reports!", category='info')
        return redirect(url_for('premium_page'))
    
    
    user_skills = Skill.query.filter_by(user_id=current_user.id).all()

    if not user_skills:
        flash('Add some skills and log progress to generate reports!', category = 'info')
        return redirect(url_for('add_skill_page'))
    

    #Get all progress entries for the user
    all_progress = []

    for skill in user_skills:
        for progress in skill.progress_entries:
            all_progress.append({
                'skill_name': skill.name,
                'category': skill.category,
                'date': progress.date,
                'hours_spent': progress.hours_spent,
                'difficulty_rating': progress.difficulty_rating,
                'target_hours': skill.target_hours,
                'total_logged':skill.total_hours_logged,
                'completion_rate': skill.progress_percentage
            })
    
    if not all_progress:
        flash('Log some progress to see detailed reports!', category = 'info')
        return redirect(url_for('log_progress_page'))
    
    #Creating the dataframe for analysis
    df = pd.DataFrame(all_progress)


    #Analysis 1: Learning Velocity (hrs per day)
    df['date'] = pd.to_datetime(df['date'])
    daily_hours = df.groupby('date')['hours_spent'].sum().reset_index()
    avg_daily_hours = daily_hours['hours_spent'].mean()


    #Analysis 2: Most/Least productive days
    df['day_of_week'] = df['date'].dt.day_name()
    productivity_by_day = df.groupby('day_of_week')['hours_spent'].sum().sort_values(ascending = False)


    #Analysis 3: Category Performance
    category_stats = df.groupby('category').agg({
        'hours_spent' : ['sum', 'mean', 'count'],
        'difficulty_rating': 'mean',
        'completion_rate': 'mean'
    }).round(2)


    #Analysis 4: Goal achievement prediction
    skills_analysis = []

    for skill in user_skills:
        if skill.total_hours_logged > 0 and skill.progress_entries:

            skill_progress = [p for p in all_progress if p['skill_name'] == skill.name]
            skill_df = pd.DataFrame(skill_progress)

            days_learning = len(skill_df)
            hours_per_day = skill.total_hours_logged / days_learning if days_learning > 0 else 0
            remaining_hours = max(0, skill.target_hours - skill.total_hours_logged)
            
            if hours_per_day > 0:
                estimated_days = remaining_hours / hours_per_day
                estimated_completion = datetime.now().date() + timedelta(days=int(estimated_days))
            else:
                estimated_completion = None
            
            skills_analysis.append({
                'name': skill.name,
                'progress': skill.progress_percentage,
                'hours_logged': skill.total_hours_logged,
                'target_hours': skill.target_hours,
                'remaining_hours': remaining_hours,
                'learning_rate': round(hours_per_day,2),
                'estimated_completion': estimated_completion
            })


    #Analysis 5: Recent Performance Trends
    last_7_days = datetime.now().date() - timedelta(days = 7)
    recent_df = df[df['date'] >= pd.to_datetime(last_7_days)]
    recent_hours = recent_df['hours_spent'].sum()
    recent_average = recent_df.groupby('date')['hours_spent'].sum().mean() if not recent_df.empty else 0



    #Data to pass to .html file
    reports_data = {
        'total_skills': len(user_skills),
        'total_hours_logged': sum(skill.total_hours_logged for skill in user_skills),
        'avg_daily_hours': round(avg_daily_hours,2),
        'most_productive_day': productivity_by_day.index[0] if not productivity_by_day.empty else 'N/A',
        'least_productive_day': productivity_by_day.index[-1] if not productivity_by_day.empty else 'N/A',
        'category_performance': category_stats.to_dict() if not category_stats.empty else {},
        'productivity_by_day': productivity_by_day.to_dict(),
        'recent_hours': recent_hours,
        'recent_avg': (recent_average, 2),
        'skills_analysis': skills_analysis
    }
    
    return render_template('reports.html', reports_data = reports_data)






@app.route('/export/csv')
@login_required
def export_csv():
    user_skills = Skill.query.filter_by(user_id = current_user.id).all()

    if not user_skills:
        flash("No data to export!", category = 'warning')
        return redirect(url_for('reports_page'))
    

    export_data = []
    for skill in user_skills:
        for progress in skill.progress_entries:
            export_data.append({
                'Date': progress.date,
                'skill Name': skill.name,
                'Category': skill.category,
                'Hours Spent': progress.hours_spent,
                'Difficulty Rating': progress.difficulty_rating,
                'Notes': progress.notes,
                'Target Hours': skill.target_hours,
                'Total Hours Logged': skill.total_hours_logged,
                'Progress Percentage': round(skill.progress_percentage,2)
            })
    
    df = pd.DataFrame(export_data)
    csv_data = df.to_csv(index=False)

    response = make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=skilltrail_data_{datetime.now().strftime('%Y-%m-%d')}.csv'

    return response






@app.route("/premium")
@login_required
def premium_page():
    if current_user.is_premium:
        return redirect(url_for('reports_page'))
    return render_template('premium.html')



@app.route('/subscribe')
@login_required
def subscribe():
    current_user.is_premium = True
    db.session.commit()
    
    flash("Payment successful! You now have access to Premium Reports!", category='success')
    return redirect(url_for('reports_page'))

    

# Database initialization route
@app.route('/init-db')
def init_database():
    try:
        db.create_all()
        return "Database tables created successfully!"
    except Exception as e:
        return f"Error creating database: {str(e)}"





# #Route for keeping my service 24/7 active 
@app.route('/keep-alive')
def keep_alive():
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "message": "SkillTrail server is running"
    }