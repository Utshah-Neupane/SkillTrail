from container import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=30), nullable = False, unique = True)
    email_address = db.Column(db.String(length=50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length=60), nullable = False)
    is_premium = db.Column(db.Boolean(), default = False)
    #Relationship of this table with skill table
    skills = db.relationship('Skill', backref='owner',
                lazy = True, cascade = 'all, delete-orphan')
    

    @property
    def password(self):
        raise AttributeError("Password is not readable!")

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, password_to_check):
        return bcrypt.check_password_hash(self.password_hash, password_to_check)




class Skill(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length=100), nullable = False)
    description = db.Column(db.Text(), nullable = True)
    category = db.Column(db.String(length = 50), nullable = True)
    target_hours = db.Column(db.Integer(), default = 0)
    created_date = db.Column(db.DateTime(), default = datetime.now().date())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)

    progress_entries = db.relationship('Progress',
                    backref = 'skill_referred', lazy = True,
                    cascade='all, delete-orphan')

    
    def __repr__(self):
        return f"<Skill {self.name}>"
    
    @property
    def total_hours_logged(self):
        progress_hrs_input = 0
        for entry in self.progress_entries:
            progress_hrs_input += entry.hours_spent
        return progress_hrs_input
    
    @property
    def progress_percentage(self):
        if self.target_hours == 0:
            return 0
        return min(100, (self.total_hours_logged / self.target_hours)*100)


 
class Progress(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, default=lambda: datetime.now().date())
    hours_spent = db.Column(db.Float(), nullable=False, default=0.0)
    notes = db.Column(db.Text(), nullable=True)
    difficulty_rating = db.Column(db.Integer(), nullable=True)  # 1-5 scale
    
    skill_id = db.Column(db.Integer(), db.ForeignKey('skill.id'), nullable=False)


    def __repr__(self):
        return f"<Progress {self.date} - {self.hours_spent} hours>"
    
    __table_args__ = (db.UniqueConstraint('skill_id', 'date', name = 'unique_skill_date'),)














