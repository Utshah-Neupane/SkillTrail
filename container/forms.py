from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError, Optional, NumberRange
from container.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username!")


    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address = email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email address is associated with an existing account! Please try a different email address!")


    username = StringField(label='User Name:',
        validators=[Length(min=2, max=30), DataRequired()])
    
    email_address = StringField(label='Email Address:',
        validators=[Email(), DataRequired()])
    
    password1 = PasswordField(label='Password:',
        validators=[Length(min=6), DataRequired()])
    
    password2 = PasswordField(label='Confirm Password:',
        validators=[EqualTo("password1"), DataRequired()])
    
    submit = SubmitField(label='Create Account')





class LoginForm(FlaskForm):
    username = StringField(label='User Name:', 
        validators=[DataRequired()])

    password = PasswordField(label='Password:',
        validators=[DataRequired()])
    
    submit = SubmitField(label='Sign In')





class AddSkillForm(FlaskForm):
    name = StringField(label = 'Skill Name:', validators = [Length(min=2, max=100),DataRequired()])
    description = TextAreaField(label = 'Description:', validators = [Length(max=500), Optional()])
    
    category = SelectField(label='Category:', 
            choices=[
                ('Programming', 'Programming'),
                ('Design', 'Design'),
                ('Marketing', 'Marketing'),
                ('Business', 'Business'),
                ('Language', 'Language'),
                ('Music', 'Music'),
                ('Other', 'Other'),
            ],
            validators=[DataRequired()]
    )
    target_hours = IntegerField(label='Target Hours:', validators=[NumberRange(min=1, max=10000), DataRequired()])

    submit = SubmitField(label="Add Skill")





class LogProgressForm(FlaskForm):
    skill_id = SelectField(label='Select Skill:', 
        coerce=int, validators=[DataRequired()])
    
    hours_spent = FloatField(label='Hours Spent:', 
        validators=[DataRequired(), NumberRange(min=0.1, max=24)])
    
    notes = TextAreaField(label='Notes/Achievements:', 
        validators=[Optional(), Length(max=1000)])
    
    difficulty_rating = SelectField(label='Difficulty Rating:', 
        choices=[
            (1, '1 - Very Easy'),
            (2, '2 - Easy'),
            (3, '3 - Medium'),
            (4, '4 - Hard'),
            (5, '5 - Very Hard')
        ], coerce=int, validators=[Optional()])
    
    submit = SubmitField(label='Log Progress')

