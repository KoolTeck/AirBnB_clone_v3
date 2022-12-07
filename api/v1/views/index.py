#!/usr/bin/python3
""" Index file """

from api.v1.views import app_views
from models import storage
from flask import jsonify

classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }


@app_views.route("/status")
def status():
    """return status in json"""
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route("/stats")
def endpoint():
    """endpoint that retrieves the number of each objects by type"""
    dic = {}
    for k, v in classes.items():
        dic[k] = storage.count(v)
    return jsonify(dic)
