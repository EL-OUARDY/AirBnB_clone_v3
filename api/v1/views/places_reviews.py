#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Review objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    # check if place object exists
    if place is None:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by id"""
    review = storage.get(Review, review_id)

    # check if review object exists
    if review is None:
        abort(404)

    # return the review object
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)

    # check if review object exists
    if review is None:
        abort(404)

    # delete the review object
    review.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """Creates a Review object"""

    # check if place exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    new_review = request.get_json()

    # validate the posted review data
    if not new_review:
        abort(400, "Not a JSON")
    elif "user_id" not in new_review.keys():
        abort(400, "Missing user_id")
    elif "text" not in new_review.keys():
        abort(400, "Missing text")
    else:
        # check if user exists
        user = storage.get(User, new_review.get("user_id", None))
        if user is None:
            abort(404)

        # create the review object
        new_review = Review(**new_review)
        new_review.place_id = place_id
        new_review.save()

    # return the new review object with CREATED status code 201
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""

    review = storage.get(Review, review_id)

    # check if review object exists
    if review is None:
        abort(404)

    new_review_data = request.get_json()

    # validate the posted review data
    if not new_review_data:
        abort(400, "Not a JSON")
    else:
        # update the review object
        for k, v in new_review_data.items():
            if k not in [
                "id",
                "place_id",
                "user_id",
                "created_at",
                "updated_at",
            ]:
                setattr(review, k, v)
        storage.save()

    # return the updated review
    return jsonify(review.to_dict())
