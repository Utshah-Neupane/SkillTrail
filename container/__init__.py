from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///container.db'
#So that users can't tamper session data stored on their browser
#For flask-forms, protection to generate secure tokens
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'



from container import routes, models

# Create database tables if they don't exist
with app.app_context():
    db.create_all()























