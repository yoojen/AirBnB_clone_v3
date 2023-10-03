#!/usr/bin/python3
"""
creates view for places
"""
from api.v1.views import app_views
from models.place import Place
from models import storage
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place_by_cities(city_id):
    """
    return all places by cities
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    obj = []
    place = storage.all(Place)
    if place is None:
        abort(404)
    for single in place.values():
        if single.city_id == city_id:
            obj.append(single.to_dict())
    return jsonify(obj), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def all_places(place_id):
    """
    returns all cities in the storage
    """
    try:
        place = storage.get('Place', place_id)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    post place object in the storage
    """
    city = storage.get(City, city_id)
    place = storage.all(Place)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify(error="Not a JSON"), 400
    if 'user_id' not in request.json:
        return({"error": "Missing user_id"}), 400
    user = storage.get(User, request.json()['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return ({"error": "Missing name"}), 400
    data = request.get_json()
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    update a place object from the storage
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
