from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

#Now I'm switching to neon database so commenting this line
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///container.db'
# Use Neon PostgreSQL in production, SQLite locally
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///container.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url


#So that users can't tamper session data stored on their browser
#For flask-forms, protection to generate secure tokens
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


from container import routes, models

with app.app_context():
    db.create_all()

# Start cron job for keeping server alive
if os.environ.get('RENDER'):  # Only run on Render, not locally
    from container.cron import start_cron_job
    start_cron_job()














