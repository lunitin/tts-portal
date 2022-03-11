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
    
    def is_admin(self):
        return (self.security_level)
    

class Access(db.Model):
    __tablename__ = "access"
    access_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverage.coverage_id'))

    def get_id(self):
        return (self.access_id)


class Coverage(db.Model):
    __tablename__ = "coverage"
    coverage_id = db.Column(db.Integer, primary_key=True)
    coverage_name = db.Column(db.String(24))
    
    def get_id(self):
        return (self.coverage_id)


class Region(db.Model):
    __tablename__ = "region"
    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(24))
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverage.coverage_id'))

    def get_id(self):
        return (self.region_id)
    

class Signal(db.Model):
    __tablename__ = "signals"
    signal_id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer)
    SignalID = db.Column(db.Integer, unique=True)

    def get_id(self):
        return(self.sig_id)
        

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    vehicle_id = db.Column(db.Integer, primary_key=True)
    vehID = db.Column(db.Integer, unique=True)
    delay = db.Column(db.Float)
    red_arrival = db.Column(db.String(3))
    split_failure = db.Column(db.String(3))
    signal_id = db.Column(db.Integer, db.ForeignKey('signal.SignalID'))
    approach_direction = db.Column(db.String(10))
    travel_direction = db.Column(db.Float)
    ett = db.Column(db.Float)
    travel_time = db.Column(db.Float)
    exit_status = db.Column(db.String(6))
    day = db.Column(db.Integer)
    stops = db.Column(db.Integer)
    u_turn = db.Column(db.String(3))
    entry_time = db.Column(db.DateTime)
    exit_time = db.Column(db.DateTime)
    
    def get_id(self):
        return(self.vehicle_id)
