#!/usr/bin/python3
"""
This module handles all default RESTFul API actions
for Place-Amenity objects
"""

from os import environ
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False
)
def get_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    # check if place exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        amenities = [obj.to_dict() for obj in place.amenities]
    else:  # file storage
        amenities = [
            storage.get(Amenity, amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]
    return jsonify(amenities)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_amenity(place_id, amenity_id):
    """Retrieves the list of all Amenity objects of a Place"""

    # check if place exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # check if amenity exists
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        # check if amenity belongs to that place
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:  # file storage
        # check if amenity belongs to that place
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def post_amenity(place_id, amenity_id):
    """Link an Amenity object to a Place"""
    # check if place exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # check if amenity exists
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if environ.get("HBNB_TYPE_STORAGE") == "db":
        # amenity is already linked to the Place
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:  # file storage
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
