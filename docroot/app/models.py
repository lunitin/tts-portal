""" models.py

Python objects for the SQLAlchemy database models

"""

from turtle import delay
from flask_login import UserMixin
from sqlalchemy_utils import JSONType
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

class Vehicle(db.Model):
    __tablename__ = "vehicles"
    # primary keys are required by SQLAlchemy
    vehicle_data_id = db.Column(db.Integer, primary_key=True)
    coverage_id = db.Column(db.Integer)
    veh_id = db.Column(db.String(length=64))
    delay = db.Column(db.Float(precision=3))
    red_arrival = db.Column(db.Boolean)
    split_failure = db.Column(db.Boolean)
    signal_id = db.Column(db.Integer)
    approach_direction = db.Column(db.String(length=10))
    ett = db.Column(db.Float(precision=3))
    travel_time = db.Column(db.Float(precision=3))
    exit_status = db.Column(db.Boolean)
    day = db.Column(db.Integer)
    stops = db.Column(db.Boolean)
    uturn = db.Column(db.Boolean)
    entry_time = db.Column(db.DateTime)
    exit_time = db.Column(db.DateTime)

    def get_id(self):
        return (self.veh_id)
    
class Coverage(db.Model):
    __tablename__ = 'coverages'
    coverage_id = db.Column(db.Integer, primary_key=True)
    coverage_name = db.Column(db.String(length=24))
    signals = db.Column(JSONType)
    
    def get_id(self):
        return(self.coverage_id)

class Signal(db.Model):
    __tablename__ = 'signals'
    signal_id = db.Column(db.Integer, primary_key=True)
    coverages = db.Colummn(JSONType)
    
    def get_id(self):
        return(self.signal_id)


class Access(db.Model):
    __tablename__ = 'access'
    access_id = db.Column(db.Integer, primary_key=True)
    user_ids = db.Column(JSONType)
    coverage_ids = db.Column(JSONType)
    
    def get_access(self):
        return(self.access_id)
