#!/usr/bin/python3
"""User module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """get information for all users"""
    users = []
    for obj in storage.all(User).values():
        users.append(obj.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """get information for the specified user"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """delete user by id"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user_create():
    """create a new user"""
    conten = request.get_json()
    if conten is None:
        return "Not a JSON", 400
    if conten.get('email') is None:
        return "Missing email", 400
    if conten.get('password') is None:
        return "Missing password", 400
    else:
        user = User(**conten)
        user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update a user"""
    if request.get_json() is None:
        return "Not a JSON", 400
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict()), 200
