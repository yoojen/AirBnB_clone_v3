#!/usr/bin/python3
"""
creates view for states
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    return all states
    """
    obj = []
    for state in storage.all(State).values():
        obj.append(state.to_dict())
    return jsonify(obj)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """
    get state accoeding to id provided
    """
    obj = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    post state to the storage
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    elif request.get_json().get('name') is None:
        return jsonify({"error": "Missing name"}), 400
    else:
        data = request.get_json()
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    update a state from the storage
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    delete state objects from storage
    """
    try:
        state = storage.get('State', state_id)
        storage.delete(state)
        return jsonify({}), 200
    except Exception:
        abort(404)
