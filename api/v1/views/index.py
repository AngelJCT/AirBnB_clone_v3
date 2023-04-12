#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"amenities": "Amenity", "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State", "users": "User"}


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON: status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns a JSON with the numbers of objects by type"""
    stats_dict = {}
    for k, v in classes.items():
        stats_dict[k] = storage.count(v)
    return jsonify(stats_dict)
