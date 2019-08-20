from datetime import datetime
from restapi.database import db


class ObservationType(db.Model):
    __tablename__ = 'observationtypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)

    def __init__(self, name,):
        self.name = name

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}"}}'.format(__class__.__name__, self.id, self.name)


class ObservedLocation(db.Model):
    __tablename__ = 'observedlocations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    lat = db.Column(db.Float, unique=False)
    lon = db.Column(db.Float, unique=False)
    observation_type = db.Column(db.Integer, db.ForeignKey('observationtypes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, lat, lon, observation_type, user_id):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.observation_type = observation_type
        self.user_id = user_id

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "lat": "{}", "lon": "{}", "observation_type": "{}", "user_id": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.lat, self.lon, self.observation_type, self.user_id)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    lat = db.Column(db.Float, unique=False)
    lon = db.Column(db.Float, unique=False)
    observed_locations = db.relationship('ObservedLocation', backref='locations', lazy=True)

    def __init__(self, name, lat, lon, observed_locations):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.observed_locations = observed_locations

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "lat": "{}", "lon": "{}", "observed_locations": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.lat, self.lon, self.observed_locations)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    role = db.Column(db.Integer, unique=False)
    observed_locations = db.relationship('ObservedLocation', backref='users', lazy=True)

    def __init__(self, name, role, observed_locations):
        self.name = name
        self.role = role
        self.observed_locations = observed_locations

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "role": "{}", "observed_locations": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.role, self.observed_locations)
