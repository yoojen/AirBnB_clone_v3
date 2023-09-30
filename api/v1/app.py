#!/usr/bin/python3
""" center of app! which used to connect to api"""
import os
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
apphost = os.getenv('HBNB_API_HOST', '0.0.0.0')
appport = int(os.getenv('HBNB_API_PORT', '5000'))


@app.teardown_appcontext
def close_session(self):
    """
    tear down ongoing session
    """
    storage.close()


@app.errorhandler(404)
def not_found(nopage):
    """
    return status of 404 if page not found
    """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    app.run(host=apphost, port=appport, threaded=True)
