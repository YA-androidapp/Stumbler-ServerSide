from datetime import datetime
from restapi.database import db


class ObservedWifi(db.Model):
    __tablename__ = 'observedwifis'
    id = db.Column(db.Integer, primary_key=True)
    bssid = db.Column(db.String(80), unique=False)
    ssid = db.Column(db.String(80), unique=False)
    lat = db.Column(db.Float, unique=False)
    lon = db.Column(db.Float, unique=False)
    rssi = db.Column(db.String(800), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    def __init__(self, bssid, ssid, lat, lon, rssi, user_id, location_id):
        self.bssid = bssid
        self.ssid = ssid
        self.lat = lat
        self.lon = lon
        self.rssi = rssi
        self.user_id = user_id
        self.location_id = location_id

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "bssid": "{}", "ssid": "{}", "lat": "{}", "lon": "{}", "rssi": "{}", "user_id": "{}", "location_id": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.lat, self.lon, self.rssi, self.user_id, self.location_id)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    lat = db.Column(db.Float, unique=False)
    lon = db.Column(db.Float, unique=False)
    observed_wifis = db.relationship('ObservedWifi', backref='locations', lazy=True)

    def __init__(self, name, lat, lon, observed_wifis):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.observed_wifis = observed_wifis

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "lat": "{}", "lon": "{}", "observed_wifis": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.lat, self.lon, self.observed_wifis)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    role = db.Column(db.Integer, unique=False)
    observed_wifis = db.relationship('ObservedWifi', backref='users', lazy=True)

    def __init__(self, name, role, observed_wifis):
        self.name = name
        self.role = role
        self.observed_wifis = observed_wifis

    def __repr__(self):
        return '{{"class": "{}", "id": "{}", "name": "{}", "role": "{}", "observed_wifis": "{}"}}'.format(
            __class__.__name__, self.id, self.name, self.role, self.observed_wifis)
