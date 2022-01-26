""" __init__.py

Flask application initilizaton and configuration variables

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Prepare for SQL Alchemy
db = SQLAlchemy()

app = Flask(__name__)

# Configuration Variables
app.config['SECRET_KEY'] = 'w057tweifvsk;erbg1[935fzsdknvbqo;34]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:beastm0de@db/tts_portal'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False;

db.init_app(app)

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
