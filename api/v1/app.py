#!/usr/bin/python3
"""This script starts a Flask web application"""

from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# pretty-print JSON responses
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


# register blueprints
app.register_blueprint(app_views)

# enable CORS for URLs starting with /api/
# and allow requests from 0.0.0.0
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """Remove the current SQLAlchemy Sessionn after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, port, debug=True, threaded=True)
