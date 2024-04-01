#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Place objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a single Place object by id"""
    place = storage.get(Place, place_id)
    # check if place object exists
    if place is None:
        abort(404)

    # return the place object
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)

    # check if place object exists
    if place is None:
        abort(404)

    # delete the place object
    place.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Creates a Place object"""

    # check if city exists
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    new_place = request.get_json()

    # validate the posted place data
    if not new_place:
        abort(400, "Not a JSON")
    elif "user_id" not in new_place.keys():
        abort(400, "Missing user_id")
    elif "name" not in new_place.keys():
        abort(400, "Missing name")
    else:
        # check if user exists
        user = storage.get(User, new_place.get("user_id", None))
        if user is None:
            abort(404)
        # create the place object
        new_place = Place(**new_place)
        new_place.city_id = city_id
        new_place.save()

    # return the new place object with CREATED status code 201
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""

    place = storage.get(Place, place_id)

    # check if place object exists
    if place is None:
        abort(404)

    new_place_data = request.get_json()

    # validate the posted place data
    if not new_place_data:
        abort(400, "Not a JSON")
    else:
        # update the place object
        for k, v in new_place_data.items():
            if k not in [
                "id",
                "user_id",
                "city_id",
                "created_at",
                "updated_at",
            ]:
                setattr(place, k, v)
        storage.save()

    # return the updated place
    return jsonify(place.to_dict())
