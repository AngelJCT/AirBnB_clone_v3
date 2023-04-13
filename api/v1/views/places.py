#!/usr/bin/python3
"""Module to retrieve an object into a valid JSON"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """Retrieves the list of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_city = []
    for place in city.places:
        places_city.append(place.to_dict())
    return jsonify(places_city)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves the list of all places in a city"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Retrieves the list of all places in a city"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    else:
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(city_id, **data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """Retrieves the list of all places in a city"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


if __name__ == '__main__':
    app_views.run(host='0.0.0.0')
