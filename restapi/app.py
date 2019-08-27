#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import User, Location, ObservedWifi
from restapi.database import db, init_db
import io


URL_PREFIX = '/v1'
URL_PREFIX_USER = URL_PREFIX + '/user'
URL_PREFIX_LOCATION = URL_PREFIX + '/location'


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('restapi.config.Config')
    init_db(app)

    return app

app = create_app()


@app.route('/')
def root():
    return redirect(url_for('user_get_all'))


@app.route(URL_PREFIX)
def v1():
    return redirect(url_for('user_get_all'))


@app.route(URL_PREFIX_USER, methods=['POST'])
def user_post():
    global app, db

    data = request.get_json()
    name = '#NAME#' if ('name' not in data) or data['name'] is None or str(data['name']) == '' else str(data['name'])
    role = 1 if ('role' not in data) or data['role'] is None or str(data['role']).isnumeric() == False else int(data['role'])

    user = User(name, role, [])
    db.session.add(user)
    db.session.commit()

    return jsonify({'r': 'Created'}), 201


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['GET'])
def user_get(id):
    global app, db

    if id != '':
        user = User.query.get(id)
        if isinstance(user, type(None)):
            return jsonify({'r': 'GET fail, no id found', 'id': id}), 403

        return jsonify({'r': 'GET success', 'id': user.id, 'name': user.name, 'role': user.role}), 200


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['PUT'])
def user_put(id):
    global app, db

    if id != '':
        user = User.query.get(id)
        print('user: {}'.format(user))
        if isinstance(user, type(None)):
            return user_post()

        data = request.get_json()
        if 'name' in data:
            user.name = '#NAME#' if data['name'] is None or str(data['name']) == '' else str(data['name'])
        if 'role' in data:
            user.role = '#ROLE#' if data['role'] is None or str(data['role']).isnumeric() == False else int(data['role'])
        db.session.commit()
        return jsonify({'r': 'PUT success', 'id': user.id, 'name': user.name, 'role': user.role}), 204


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['DELETE'])
def user_delete(id):
    global app, db

    if id != '':
        user = User.query.get(id)
        if isinstance(user, type(None)):
            return jsonify({'r': 'DELETE fail, no id found', 'id': id}), 403

        db.session.delete(user)
        db.session.commit()
        return jsonify({'r': 'DELETE success'}), 200


@app.route(URL_PREFIX_USER, methods=['GET'])
def user_get_all():
    global app, db

    # if request.method == 'GET':
    d = {'r': 'GET success'}
    d['data'] = [{'id': i.id, 'name': i.name, 'role': i.role} for i in User.query.all()]
    return jsonify(d), 200



@app.route(URL_PREFIX_LOCATION, methods=['POST'])
def location_post():
    global app, db

    data = request.get_json()
    name = '#' if ('name' not in data) or data['name'] is None or str(data['name']) == '' else str(data['name'])
    lat = 180 if ('lat' not in data) or data['lat'] is None or isfloat(data['lat']) == False else float(data['lat'])
    lon = 90 if ('lon' not in data) or data['lon'] is None or isfloat(data['lon']) == False else float(data['lon'])

    location = Location(name, lat, lon, [])
    db.session.add(location)
    db.session.commit()

    return jsonify({'r': 'Created'}), 201


@app.route(URL_PREFIX_LOCATION+'/<string:id>', methods=['GET'])
def location_get(id):
    global app, db

    if id != '':
        location = Location.query.get(id)
        if isinstance(location, type(None)):
            return jsonify({'r': 'GET fail, no id found', 'id': id}), 403

        return jsonify({'r': 'GET success', 'id': location.id, 'name': location.name, 'lat': location.lat, 'lon': location.lon, 'observed_wifis': location.observed_wifis}), 200


@app.route(URL_PREFIX_LOCATION+'/<string:id>', methods=['PUT'])
def location_put(id):
    global app, db

    if id != '':
        location = Location.query.get(id)
        print('location: {}'.format(location))
        if isinstance(location, type(None)):
            return location_post()

        data = request.get_json()
        if 'name' in data:
            location.name = '#NAME#' if data['name'] is None or str(data['name']) == '' else str(data['name'])
        if 'lat' in data:
            location.lat = 180 if data['lat'] is None or isfloat(data['lat']) == False else float(data['lat'])
        if 'lon' in data:
            location.lon = 90 if data['lon'] is None or isfloat(data['lon']) == False else float(data['lon'])
        db.session.commit()
        return jsonify({'r': 'PUT success', 'id': location.id, 'name': location.name, 'lat': location.lat, 'lon': location.lon}), 204


@app.route(URL_PREFIX_LOCATION+'/<string:id>', methods=['DELETE'])
def location_delete(id):
    global app, db

    if id != '':
        location = Location.query.get(id)
        if isinstance(location, type(None)):
            return jsonify({'r': 'DELETE fail, no id found', 'id': id}), 403

        db.session.delete(location)
        db.session.commit()
        return jsonify({'r': 'DELETE success'}), 200


@app.route(URL_PREFIX_LOCATION, methods=['GET'])
def location_get_all():
    global app, db

    d = {'r': 'GET success'}
    d['data'] = [{'id': i.id, 'name': i.name, 'lat': i.lat, 'lon': i.lon, 'observed_wifis': i.observed_wifis} for i in Location.query.all()]
    return jsonify(d), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'r': '404 Not found'}), 404
