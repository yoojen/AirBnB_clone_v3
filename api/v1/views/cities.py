#!/usr/bin/python3
"""
creates view for states
"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_by_states(state_id):
    """
    return all cities by states
    """
    obj = []
    city = storage.all(City)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for single in city.values():
        if single.state_id == state_id:
            obj.append(single.to_dict())
            print(obj)
    return jsonify(obj)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def all_cities(city_id):
    """
    returns all cities in the storage
    """
    cities = []
    for city in storage.all(City).values():
        if city_id == city.id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    post city object in the storage
    """
    city = storage.all(City)
    if city is None:
        abort(400)
    if not request.json:
        return jsonify(error="Not a JSON"), 400
    if 'name' not in request.json:
        return("Missing name"), 400
    data = request.get_json()
    new_city = City(state_id=state_id,**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    update a city object from the storage
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if city is None:
        return jsonify(error="Not a JSON"), 400
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
