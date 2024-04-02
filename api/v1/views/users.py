#!/usr/bin/python3
"""This module handles all default RESTFul API actions for User objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users_dict = storage.all(User)
    return jsonify([obj.to_dict() for obj in users_dict.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a single User object by id"""
    user = storage.get(User, user_id)

    # check if user object exists
    if user is None:
        abort(404)

    # return the user object
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)

    # check if user object exists
    if user is None:
        abort(404)

    # delete the user object
    user.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User object"""
    new_user = request.get_json()

    # validate the posted user data
    if not new_user:
        abort(400, "Not a JSON")
    elif "email" not in new_user.keys():
        abort(400, "Missing email")
    elif "password" not in new_user.keys():
        abort(400, "Missing password")
    else:
        # create the user object
        new_user = User(**new_user)
        new_user.save()

    # return the new user object with CREATED status code 201
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""

    user = storage.get(User, user_id)

    # check if user object exists
    if user is None:
        abort(404)

    new_user_data = request.get_json()

    # validate the posted user data
    if not new_user_data:
        abort(400, "Not a JSON")
    else:
        # update the user object
        for k, v in new_user_data.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, k, v)
        storage.save()

    # return the updated user
    return jsonify(user.to_dict())
