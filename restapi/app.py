#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import User
from restapi.database import db, init_db
import io


URL_PREFIX = '/v1'
URL_PREFIX_USER = URL_PREFIX + '/user'
URL_PREFIX_LOCATION = URL_PREFIX + '/location'


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('restapi.config.Config')
    init_db(app)

    return app

app = create_app()

@app.route(URL_PREFIX_USER, methods=['POST'])
def user_post():
    global app, db

    # if request.method == 'POST':
    data = request.get_json()
    print('data: {}'.format(data))
    name = '#NAME#' if not data['name'] else data['name']
    role = 1 if not data['role'] or data['role'].isnumeric() == False else data['role']

    user = User(name, role, None)
    db.session.add(user)
    db.session.commit()

    return jsonify({'r': 'Created'}), 201


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['GET'])
def user_get(id):
    global app, db

    # if request.method == 'GET':
    if id != '':
        user = User.query.get(id)
        if isinstance(user, type(None)):
            return jsonify({'r': 'GET fail, no id found', 'id': id}), 403

        r = {
            'r': 'GET success',
            'id': user.id,
            'name': user.name,
            'role': user.role
        }

        return jsonify(r), 200


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['PUT'])
def user_put(id):
    global app, db

    # if request.method == 'PUT':
    if id != '':
        user = User.query.get(id)
        print('user: {}'.format(user))
        if isinstance(user, type(None)):
            return post()

        data = request.get_json()
        # id = '#ID#' if not data['id'] else data['id']
        name = '#NAME#' if not data['name'] else data['name']
        role = '#ROLE#' if not data['role'] else data['role']

        # user.id = id
        user.name = name
        user.role = role

        # db.session.add(user)
        db.session.commit()
        return jsonify({'r': 'PUT success', 'id': id, 'name': name, 'role': role}), 204


@app.route(URL_PREFIX_USER+'/<string:id>', methods=['DELETE'])
def user_delete(id):
    global app, db

    # if request.method == 'DELETE':
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

    d = {'r': 'GET success'}
    d['data'] = [{'id': i.id, 'name': i.name, 'role': i.role} for i in User.query.all()]
    return jsonify(d), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'r': '404 Not found'}), 404
