#!/usr/bin/python3
"""This module handles all default RESTFul API actions for State objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all():
    """Retrieves the list of all State objects"""
    states_dict = storage.all(State)
    return jsonify([obj.to_dict() for obj in states_dict.values()])


@app_views.route(
    "/states/<string:state_id>", methods=["GET"], strict_slashes=False
)
def get_state(state_id):
    """Retrieves a single State object"""
    state = storage.get(State, state_id)

    # check if state object exists
    if state is None:
        abort(404)

    # return the state object
    return jsonify(state.to_dict())


@app_views.route(
    "/states/<string:state_id>", methods=["DELETE"], strict_slashes=False
)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)

    # check if state object exists
    if state is None:
        abort(404)

    # delete the state object
    state.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State object"""
    new_state = request.get_json()

    # validate the posted state data
    if not new_state:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        # create the state object
        new_state = State(**new_state)
        new_state.save()

    # return the new state object with CREATED status code 201
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route(
    "/states/<string:state_id>", methods=["PUT"], strict_slashes=False
)
def update_state(state_id):
    """Updates a State object"""

    state = storage.get(State, state_id)

    # check if state object exists
    if state is None:
        abort(404)

    new_state_data = request.get_json()

    # validate the posted state data
    if not new_state_data:
        abort(400, "Not a JSON")
    else:
        # update the state object
        for k, v in new_state_data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(state, k, v)
        storage.save()

    # return the updated state
    return jsonify(state.to_dict())
