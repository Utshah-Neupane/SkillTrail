from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///container.db'

#So that users can't tamper session data stored on their browser
#For flask-forms, protection to generate secure tokens
app.config['SECRET_KEY'] = 'ca6db900e69ab97455788434'   

db = SQLAlchemy(app)


from container import routes, models




















