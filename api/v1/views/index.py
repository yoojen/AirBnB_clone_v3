#!/usr/bin/python3
""" returns json statuses and stats for app_views routes  """
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def showStatus():
    """
    show the status of api
        statatus: OK
    """
    obj = {"status": "OK"}
    return jsonify(obj)


@app_views.route('/stats',  methods=['GET'], strict_slashes=False)
def showStats():
    """
    show stats of objects
        return type: JSON
    """
    obj = {
            "amenities": storage.count('Amenityi'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }
    return jsonify(obj)


if __name__ == "__main__":
    pass
