#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ All amenity """
    amenitys = []
    for amenity in storage.all("Amenity").values():
        amenitys.append(amenity.to_dict())
    return jsonify(amenitys)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id=None):
    """ amenity by id """
    get_amenity = storage.get(Amenity, amenity_id)
    if get_amenity is None:
        abort(404)
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """ Function that delete amenity by id"""
    del_amenity = storage.all("Amenity").values()
    obj = [obje.to_dict() for obje in del_amenity if obje.id == amenity_id]
    if obj == []:
        abort(404)
    for obje in del_amenity:
        if obje.id == amenity_id:
            storage.delete(obje)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """function that create amenities"""
    post_data = request.get_json()
    if post_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_name = post_data.get('name')
    if new_name is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**post_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id):
    """Fuction that update amenities"""
    set_amenity = storage.get(Amenity, amenity_id)
    if set_amenity is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in put_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(set_amenity, key, value)
    set_amenity.save()
    return jsonify(set_amenity.to_dict())
