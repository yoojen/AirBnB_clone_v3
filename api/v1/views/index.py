from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def showStatus():
    """
    showthe status of api
    """
    obj = {"status": "OK"}
    return jsonify(obj)

@app_views.route('/stats', strict_slashes=False)
def showStats():
    """
    show stats of objects
    """
    obj = {
            "amenities": storage.count('Amenityi'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews":storage. count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')
            }
    return jsonify(obj)
