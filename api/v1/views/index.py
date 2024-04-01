#!/usr/bin/python3
"""This module contains api endpoints"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """return status OK as json"""
    return jsonify({"status": "OK"})
