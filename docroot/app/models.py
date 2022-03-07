""" models.py

Python objects for the SQLAlchemy database models

"""

from flask_login import UserMixin
from . import db


"""
Model for Users
"""
class User(UserMixin, db.Model):
    __tablename__ = "users"

    # Primary keys are required by SQLAlchemy
    user_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    security_level = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_last_login = db.Column(db.DateTime)
    date_last_password_change = db.Column(db.DateTime)

    # Override get_id() - Flask-Login expects a different column name
    def get_id(self):
        return (self.user_id)

    def is_admin(self):
        return (self.security_level)
