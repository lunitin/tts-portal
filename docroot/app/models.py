""" models.py

Python objects for the SQLAlchemy database models

"""

from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    user_id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    security_level = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_last_login = db.Column(db.DateTime)
    date_last_password_change = db.Column(db.DateTime)

    def get_id(self):
        return (self.user_id)
