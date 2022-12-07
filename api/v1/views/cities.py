#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request, abort
from models.state import State
from models.city import City


app = Flask(__name__)


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_city():
    """ All cities """
    cities = []
    for city in storage.all("City").values():
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_by_city(state_id=None):
    """ Cities by states"""
    get_state = storage.get(State, state_id)
    if get_state is None:
        abort(404)
    cities = []
    for k in get_state.cities:
        cities.append(k.to_dict())
    return (jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id=None):
    """ cities by id """
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    return jsonify(get_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """ Function that delete a state by id"""
    del_city = storage.all("City").values()
    obj = [obje.to_dict() for obje in del_city if obje.id == city_id]
    if obj == []:
        abort(404)
    for obje in del_city:
        if obje.id == city_id:
            storage.delete(obje)
            storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """function that create a cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    new_name = post_data.get('name')
    if new_name is None:
        return jsonify({'error': 'Missing name'}), 400
    post_data['state_id'] = state_id
    new_city = City(**post_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """Fuction that update cities"""
    set_city = storage.get(City, city_id)
    if set_city is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in put_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(set_city, key, value)
    set_city.save()
    return jsonify(set_city.to_dict())
