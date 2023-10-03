#!/usr/bin/python3
"""
creates view for users
"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    retrieve all users from the storage
    """
    obj = []
    for user in storage.all(User).values():
        obj.append(user.to_dict())
    return jsonify(obj)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """
    return all users by id provided
    """
    obj = []
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    users = [single.to_dict() for single in user.values() if single.id == user_id]
    return jsonify(users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    post user object in the storage
    """
    user = storage.all(User)
    if user is None:
        abort(400)
    if not request.json:
        return jsonify(error="Not a JSON"), 400
#    if request.get_json().get('email')
    if 'email' not in request.json:
        return("Missing email"), 400
    elif 'password' not in request.json:
        return("Missing password"), 400
    new_user = User(email=request.get_json(["email"]),
                    password=request.get_json(["password"]))
    for key, value in request.get_json().items():
        setattr(new_user, key, value)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    update a user object from the storage
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200

