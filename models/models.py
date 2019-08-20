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
    observed_lat = db.Column(db.Float, unique=False)
    observed_lon = db.Column(db.Float, unique=False)
    observation_type = db.Column(db.Integer, db.ForeignKey('observationtype.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, observed_lat, observed_lon, observation_type, user_id):
        self.name = name
        self.observed_lat = observed_lat
        self.observed_lon = observed_lon
        self.observation_type = observation_type
        self.user_id = user_id

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "observed_lat": "{}", "observed_lon": "{}", "observation_type": "{}", "user_id": "{}"}}'.format(__class__.__name__, self.id, self.name, self.observed_lat, self.observed_lon, self.observation_type, self.user_id)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    exact_lat = db.Column(db.Float, unique=False)
    exact_lon = db.Column(db.Float, unique=False)
    observed_locations = db.relationship('ObservedLocation', backref='location', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, exact_lat, exact_lon, observed_locations, user_id):
        self.name = name
        self.exact_lat = exact_lat
        self.exact_lon = exact_lon
        self.observed_locations = observed_locations
        self.user_id = user_id

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "exact_lat": "{}", "exact_lon": "{}", "observed_locations": "{}", "user_id": "{}"}}'.format(__class__.__name__, self.id, self.name, self.exact_lat, self.exact_lon, self.observed_locations, self.user_id)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    role = db.Column(db.Integer, unique=False)
    locations = db.relationship('Location', backref='user', lazy=True)

    def __init__(self, name, role, locations):
        self.name = name
        self.role = role
        self.locations = locations

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "role": "{}", "locations": "{}"}}'.format(__class__.__name__, self.id, self.name, self.role, self.locations)
