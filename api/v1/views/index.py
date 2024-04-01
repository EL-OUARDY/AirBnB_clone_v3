#!/usr/bin/python3
"""This module contains API endpoints for status and count features"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """return status OK as json"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count():
    """retrieves the number of each objects by type"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    dictionary = {k: storage.count(v) for k, v in classes.items()}

    return jsonify(dictionary)
