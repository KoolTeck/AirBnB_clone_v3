#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request, abort
from models.state import State


app = Flask(__name__)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """ Function that get all states and states id """
    if state_id is None:
        states = storage.all("State")
        get_state = jsonify([value.to_dict() for key, value in states.items()])
        return get_state
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    return jsonify(get_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Function that delete a state by id """
    states = storage.all("State").values()
    obj = [obje.to_dict() for obje in states if obje.id == state_id]
    if obj == []:
        abort(404)
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ Function that create a state """
    post_data = request.get_json()
    if post_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    new_name = post_data.get('name')
    if new_name is None:
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**post_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Function that updates a state data """
    set_state = storage.get(State, state_id)
    if set_state is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in put_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(set_state, key, value)
    set_state.save()
    return jsonify(set_state.to_dict())
