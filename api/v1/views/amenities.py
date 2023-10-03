#!/usr/bin/python3
"""
creates view for amenity
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    """
    retrieve all amenities from the storage
    """
    obj = []
    for amenity in storage.all(Amenity).values():
        obj.append(amenity.to_dict())
    return jsonify(obj)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    return all amenities by id provided
    """
    obj = []
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for single in amenity.values():
        if single.id == amenity_id:
            obj.append(single.to_dict())
    return jsonify(obj), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    '''
        creation of amenity object in the storage
    '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """
    update a amenity object from the storage
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
