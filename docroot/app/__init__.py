""" __init__.py

Flask application initilizaton

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from . import config

# Prepare for SQL Alchemy
db = SQLAlchemy()

app = Flask(__name__)

# Import App Configuration Variables
app.config['SECRET_KEY'] = config.SESSION_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.MYSQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_DEBUG'] = config.MAIL_DEBUG
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER

# DB Initialization
db.init_app(app)

# Flask-Mail Initialization
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'anon.login'
login_manager.init_app(app)

from .models import User

# Connect LoginManager with User Model
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authenticated route blueprints
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# Anonymous route blueprints
from .anon import anon as anon_blueprint
app.register_blueprint(anon_blueprint)
