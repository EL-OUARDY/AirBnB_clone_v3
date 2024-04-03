#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Place objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


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


@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
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


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def advanced_search():
    """
    Retrieves all Place objects that meet the optional
    filter passed in the body of the request as JSON
    - states: list of State ids
    - cities: list of City ids
    - amenities: list of Amenity ids
    """

    # get posted data
    data = request.get_json()
    states = data.get("states", None)
    cities = data.get("cities", None)
    amenities = data.get("amenities", None)

    # check posted data
    if data is None:
        abort(400, "Not a JSON")

    # none of the filters is provided
    if not data or all([not states, not cities, not amenities]):
        all_places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(all_places)

    # list holds result after applying filters
    places_list = []

    if states:
        states_list = [storage.get(State, id) for id in states]
        for state in states_list:
            # check state it could be None!
            if state:
                for city in state.cities:
                    for place in city.places:
                        places_list.append(place)

    if cities:
        cities_list = [storage.get(City, id) for id in cities]
        for city in cities_list:
            # check city it could be None!
            if city:
                for place in city.places:
                    # avoid duplicates
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_list = [storage.get(Amenity, id) for id in amenities]
        temp_list = []
        for place in places_list:
            for amenity in amenities_list:
                if amenity in place.amenities:
                    temp_list.append(place)

        places_list = temp_list

    # prepare places list
    places = [place.to_dict() for place in places_list]
    # remove amenities key from each place dictionary
    [place.pop("amenities", None) for place in places if "amenities" in place]

    return jsonify(places)
