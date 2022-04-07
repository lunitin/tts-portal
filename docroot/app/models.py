""" models.py

Python objects for the SQLAlchemy database models

"""

from logging import raiseExceptions
import datetime
import json
from flask_login import UserMixin
from flask import make_response, jsonify
from . import db
from typing import List
from sqlalchemy.exc import SQLAlchemyError
import enum
from sqlalchemy import Enum


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def find_all(cls):
        try:
            all_in_table = cls.query.all()
        except SQLAlchemyError as e:
            return make_response(jsonify(str(e)), 400)
        else:
            return [c.as_dict() for c in all_in_table], 200

    @classmethod
    def find_by_id(cls, id):
        entity_by_id = cls.query.filter_by(id=id).first()
        return entity_by_id

    def get_id(self):
        try:
            entity_id = self.id
        except SQLAlchemyError as e:
            return make_response(jsonify(str(e)), 400)
        else:
            return entity_id, 200

    def as_dict(self):
        my_dict = {}
        for c in self.__table__.columns:
            if isinstance(c.type, db.DateTime):
                my_dict[c.name] = str(getattr(self, c.name))
            else:
                my_dict[c.name] = getattr(self, c.name)
        #my_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return my_dict


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify(str(e)), 400)
        else:
            return self.as_dict(), 201

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(jsonify(str(e)), 400)
        else:
            return make_response("Entity deleted successfully", 204)

access_table = db.Table('access', BaseModel.metadata,
                  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                  db.Column('coverage_id', db.Integer, db.ForeignKey('coverages.id'), primary_key=True)
)

class User(UserMixin, BaseModel):
    __tablename__ = "users"
    # primary keys are required by SQLAlchemy
    email_address = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    security_level = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=True)
    date_last_login = db.Column(db.DateTime, nullable=True)
    date_last_password_change = db.Column(db.DateTime, nullable=True)
    coverages = db.relationship('Coverage', secondary=access_table, backref='users', lazy='subquery')

    def is_admin(self):
        return (self.security_level)

    def fetch_coverages(self):
        return json.dumps([c.as_dict() for c in self.coverages])

    def add_coverages(self, coverages):
        for coverage_id in coverages:
            coverage = Coverage.find_by_id(coverage_id)
            if coverage:
                self.coverages.append(coverage)
            else:
                return(coverage_id)
        return 0 # All were added good

    def remove_coverages(self, coverages):
        for coverage_id in coverages:
            coverage = Coverage.find_by_id(coverage_id)
            if coverage:
                self.coverages.remove(coverage)
            else:
                return(coverage_id)
        return 0


class ApproachDirection(enum.Enum):
    Straight = "Straight"
    Right = "Right"
    Left = "Left"

class TravelDirection(enum.Enum):
    Northbound = "Northbound"
    Eastbound = "Eastbound"
    Southbound = "Southbound"
    Westbound = "Westbound"

class Vehicle(BaseModel):
    __tablename__ = "vehicles"
    # primary keys are required by SQLAlchemy
    veh_id = db.Column(db.String(length=64),nullable=False)
    delay = db.Column(db.Float(precision=3),nullable=True)
    red_arrival = db.Column(db.Boolean,nullable=True)
    split_failure = db.Column(db.Boolean,nullable=True)
    signal_id = db.Column(db.Integer, db.ForeignKey('signals.id'), nullable=True)
    approach_direction = db.Column(db.String(length=10), nullable=True)
    travel_direction = db.Column(db.String(length=10), nullable=True)
    ett = db.Column(db.Float(precision=3),nullable=True)
    travel_time = db.Column(db.Float(precision=3),nullable=True)
    exit_status = db.Column(db.String(length=6),nullable=True)
    day = db.Column(db.Integer,nullable=True)
    entry_time = db.Column(db.DateTime, nullable=True)
    exit_time = db.Column(db.DateTime, nullable=True)
    stops = db.Column(db.Integer,nullable=True)
    uturn = db.Column(db.Boolean,nullable=True)
    hour = db.Column(db.Integer, nullable=True)
    peak = db.Column(db.String(length=64), nullable=True)
    #travel_direction = db.Column(Enum(TravelDirection), nullable=True) # Not JSON Serializable
    #approach_direction = db.Column(Enum(ApproachDirection), nullable=True) # Not JSON Serializable


    # coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.id'), nullable=True)

    @classmethod
    def search_by(cls, EntryTime=None, ExitTime=None, TravelDirection=None, ApproachDirection=None,
            Day=None, SignalID=None, Stops=None, Uturn=None, DelayMinimum=None,
            DelayMaximum=None, RedArrival=None, ETTMinimum=None, ETTMaximum=None,
            TravelTimeMinimum=None, TravelTimeMaximum=None, ExitStatus=None, CoverageID=None,
            Peak=None, Hour=None):

        query = db.session.query(Vehicle)
        #print('Day: {}, SignalID: {}, TravelDirection: {}, ApproachDirection: {}'.format(Day, SignalID, TravelDirection, ApproachDirection))
        if EntryTime is not None: query = query.filter(Vehicle.entry_time>=EntryTime)
        if ExitTime is not None: query = query.filter(Vehicle.exit_time<=ExitTime)
        if TravelDirection is not None: query = query.filter(Vehicle.travel_direction==TravelDirection)
        if ApproachDirection is not None: query = query.filter(Vehicle.approach_direction==ApproachDirection)
        if Day is not None: query = query.filter(Vehicle.day.in_(Day))
        if SignalID is not None: query = query.filter(Vehicle.signal_id.in_(SignalID))
        if CoverageID is not None: query = query.filter(Vehicle.coverage_id.in_(CoverageID))
        if Stops is not None: query = query.filter(Vehicle.stops == Stops)
        if Uturn is not None: query = query.filter(Vehicle.uturn == Uturn)
        if DelayMinimum is not None: query = query.filter(Vehicle.delay >= DelayMinimum)
        if DelayMaximum is not None: query = query.filter(Vehicle.delay <= DelayMaximum)
        if RedArrival is not None: query = query.filter(Vehicle.red_arrival == RedArrival)
        if ETTMinimum is not None: query = query.filter(Vehicle.ett >= ETTMinimum)
        if ETTMaximum is not None: query = query.filter(Vehicle.ett <= ETTMaximum)
        if TravelTimeMinimum is not None: query = query.filter(Vehicle.travel_time >= TravelTimeMinimum)
        if TravelTimeMaximum is not None: query = query.filter(Vehicle.travel_time <= TravelTimeMaximum)
        if ExitStatus is not None: query = query.filter(Vehicle.exit_status == ExitStatus)
        if Peak is not None: query = query.filter(Vehicle.Peak == Peak)
        if Hour is not None: query = query.filter(Vehicle.Hour.in_(Hour))

        result = query.all()
        return [c.as_dict() for c in result], 200


class Signal(BaseModel):
    __tablename__ = 'signals'
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=True)
    vehicles = db.relationship('Vehicle', backref='signal', lazy='subquery')

    def add_vehicles(self, vehicles, delete_old):
        if delete_old == True:
            self.vehicles = []
        for veh_id in vehicles:
            vehicle = Vehicle.find_by_id(veh_id)
            if vehicle:
                self.vehicles.append(vehicle)
            else:
                return(veh_id)
        return 0 # All were added good

    #def remove_vehicles(self, vehicles)


class Region(BaseModel):
    __tablename__ = "region"
    region_name = db.Column(db.String(24))
    coverage_id = db.Column(db.Integer, db.ForeignKey('coverages.id'), nullable=True)
    signals = db.relationship('Signal', backref='Region', lazy='subquery')

    def get_id(self):
        return (self.region_id)


class Coverage(BaseModel):
    __tablename__ = 'coverages'
    coverage_name = db.Column(db.String(length=24), nullable=False)
    regions = db.relationship('Region', backref='coverage', lazy='subquery')

    # def add_signals(self, signals, delete_old):
    #     if delete_old == True:
    #         self.signals = []
    #     if signals:
    #         for signal_id in signals:
    #             signal = Signal.find_by_id(signal_id)
    #             if signal:
    #                 self.signals.append(signal)
    #             else:
    #                 return(signal_id)
    #     else:
    #         self.signals = []
    #     return 0 # All were added good

    #def remove_signals(self, signals) # For a later time :)
