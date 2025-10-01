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
# Handle database connection with SSL for Neon PostgreSQL
# First, check if we have a production database URL from environment variables
# Handle database connection with SSL for Neon PostgreSQL
database_url = os.environ.get('DATABASE_URL')

if database_url and database_url.startswith('postgres'):
    # Parse the URL to handle existing query parameters
    from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
    parsed = urlparse(database_url)
    
    # Get existing query parameters
    query = parse_qs(parsed.query)
    
    # Update or add sslmode parameter
    query['sslmode'] = 'require'
    
    # Rebuild the URL with updated query
    database_url = urlunparse(parsed._replace(
        query=urlencode(query, doseq=True)
    ))
    print("Using production PostgreSQL database with SSL")
else:
    # Fall back to SQLite for local development
    database_url = 'sqlite:///container.db'
    print("Using local SQLite database")

# Set the database URI in Flask config
app.config['SQLALCHEMY_DATABASE_URI'] = database_url




#So that users can't tamper session data stored on their browser
#For flask-forms, protection to generate secure tokens
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,      # Check if connection is alive before using
    'pool_recycle': 290,        # Recycle connections before database timeout (5 minutes)
    'pool_timeout': 10,         # Wait 10 seconds for a connection
    'pool_size': 5,             # Maintain up to 5 connections
    'max_overflow': 10,         # Allow up to 10 connections during peak
    'pool_use_lifo': True       # Use last-in-first-out for better connection reuse
}


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


from container import routes, models

with app.app_context():
    db.create_all()

# # Start cron job for keeping server alive
# if os.environ.get('RENDER'):  # Only run on Render, not locally
#     from container.cron import start_cron_job
#     start_cron_job()














