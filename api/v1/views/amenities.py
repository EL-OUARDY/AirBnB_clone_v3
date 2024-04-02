#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Amenity objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities_dict = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities_dict.values()])


@app_views.route(
    "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amenity(amenity_id):
    """Retrieves a single amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    # check if amenity object exists
    if amenity is None:
        abort(404)

    # return the amenity object
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    # check if amenity object exists
    if amenity is None:
        abort(404)

    # delete the amenity object
    amenity.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    new_amenity = request.get_json()

    # validate the posted amenity data
    if not new_amenity:
        abort(400, "Not a JSON")
    elif "name" not in new_amenity.keys():
        abort(400, "Missing name")
    else:
        # create the amenity object
        new_amenity = Amenity(**new_amenity)
        new_amenity.save()

    # return the new amenity object with CREATED status code 201
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Updates a Amenity object"""

    amenity = storage.get(Amenity, amenity_id)

    # check if amenity object exists
    if amenity is None:
        abort(404)

    new_amenity_data = request.get_json()

    # validate the posted amenity data
    if not new_amenity_data:
        abort(400, "Not a JSON")
    else:
        # update the amenity object
        for k, v in new_amenity_data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(amenity, k, v)
        storage.save()

    # return the updated amenity
    return jsonify(amenity.to_dict())
