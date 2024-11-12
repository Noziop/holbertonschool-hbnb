"""Where our beloved Haunted Spirit speaks to us! 🏚️."""

from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restx import Namespace, Resource, fields

from app.api import admin_only, auth_required, log_me, owner_only
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "reviews",
    validate=True,
    description="Where our beloved Haunted Spirit speaks to us! 🏚️",
)
facade = HBnBFacade()

# Modèles Swagger/OpenAPI
input_review_model = ns.model(
    "Review",
    {
        "id": fields.String(
            readonly=True,
            description="Unique review identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "user_id": fields.String(
            required=True,
            description="Ghost reviewer ID",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "place_id": fields.String(
            required=True,
            description="Haunted place ID",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "text": fields.String(
            required=True,
            min_length=10,
            description="Haunted feedback",
            example="This place is haunted!",
        ),
        "rating": fields.Integer(
            required=True, min=1, max=5, description="Spooky rating", example=5
        ),
    },
)

output_review_model = ns.model(
    "Review_output",
    {
        "id": fields.String(
            readonly=True,
            description="Unique review identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "user_id": fields.String(
            required=True,
            description="Ghost reviewer ID",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "place_id": fields.String(
            required=True,
            description="Haunted place ID",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "text": fields.String(
            required=True,
            min_length=10,
            description="Haunted feedback",
            example="This place is haunted!",
        ),
        "rating": fields.Integer(
            required=True, min=1, max=5, description="Spooky rating", example=5
        ),
        "created_at": fields.DateTime(
            readonly=True,
            description="Review creation date",
            example="2021-10-31T00:00:00Z",
        ),
        "updated_at": fields.DateTime(
            readonly=True,
            description="Review update date",
            example="2021-10-31T00:00:00Z",
        ),
    },
)

error_model = ns.model(
    "ErrorResponse",
    {
        "message": fields.String(required=True, description="Error message"),
        "reviews": fields.List(
            fields.Raw, required=True, description="Empty list for errors"
        ),
    },
)


@ns.route("/")
class ReviewList(Resource):
    """Endpoint for managing the collection of haunted reviews! 👻.

    This endpoint handles listing all reviews and creating new ones.
    Supports filtering by user, place, and rating."""

    @log_me(component="api")
    @ns.doc(
        "list_reviews",
        responses={
            200: "Success",
            400: "Invalid parameters",
            404: "No reviews found",
        },
    )
    @ns.response(200, "Success", [output_review_model])
    @ns.response(404, "Not Found", error_model)
    @ns.response(400, "Bad Request", error_model)
    @ns.param("user_id", "Ghost reviewer ID", type=str, required=False)
    @ns.param("place_id", "Haunted place ID", type=str, required=False)
    @ns.param("rating", "Spooky rating", type=int, required=False)
    def get(self):
        """List all haunted reviews with optional filtering! 👻"""
        try:
            criteria = {}
            for field in ["user_id", "place_id", "rating"]:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]

            reviews = facade.find(Review, **criteria)

            # Si reviews est None ou une liste vide
            if not reviews:
                return {
                    "message": "No haunted reviews found in our realm! 👻",
                    "reviews": [],
                }, 404

            return reviews, 200

        except Exception as e:
            return {
                "message": f"A spectral error occurred: {str(e)} 👻",
                "reviews": [],
            }, 400

    @log_me(component="api")
    @ns.doc(
        "create_review",
        responses={
            201: "Review created",
            400: "Invalid parameters",
            404: "User or Place not found",
            401: "Unauthorized",
        },
    )
    @ns.expect(input_review_model)
    @ns.marshal_with(output_review_model, code=201)
    @auth_required()
    def post(self):
        """Create a new haunted review! ✍️.

        The user_id is automatically set to the authenticated user's ID.

        Returns:
            Review: The newly created review.

        Raises:
            401: If the user is not authenticated.
            404: If the place or user doesn't exist.
            400: If the review data is invalid."""
        try:
            current_user_id = get_jwt_identity()
            data = ns.payload.copy()
            data["user_id"] = current_user_id

            # Validate place and user existence
            place = facade.get(Place, data["place_id"])
            user = facade.get(User, current_user_id)

            if not isinstance(place, Place):
                ns.abort(404, "This haunted place doesn't exist!")
            if not isinstance(user, User):
                ns.abort(404, "This ghost reviewer doesn't exist!")

            review = facade.create(Review, data)
            if not isinstance(review, Review):
                ns.abort(400, "Failed to materialize the review!")
            return review, 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
@ns.param("review_id", "The haunted review identifier")
class ReviewDetail(Resource):
    """Endpoint for managing individual haunted reviews! 👻.

    This endpoint handles retrieving, updating, and deleting
    specific reviews by their unique identifier. Only owners
    can update their reviews, while admins can delete any review."""

    @log_me(component="api")
    @ns.doc("get_review", responses={200: "Success", 404: "Review not found"})
    @ns.marshal_with(output_review_model)
    def get(self, review_id):
        """Find a specific haunted review! 🔍.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            Review: The requested haunted review.

        Raises:
            404: If the review doesn't exist or has been deleted."""
        review = facade.get(Review, review_id)
        if not isinstance(review, Review) or review.rating is None:
            ns.abort(404, "This review has vanished!")
        return review

    @log_me(component="api")
    @ns.doc(
        "update_review",
        responses={
            200: "Success",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Review not found",
        },
    )
    @ns.expect(input_review_model)
    @ns.marshal_with(output_review_model)
    @owner_only
    def put(self, review_id):
        """Update a haunted review! 📝.

        Only the review owner can update their own review.
        The user_id cannot be changed during update.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            Review: The updated haunted review.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not the review owner.
            404: If the review doesn't exist.
            400: If the update data is invalid."""
        try:
            review = facade.get(Review, review_id)
            if not isinstance(review, Review):
                ns.abort(404, "This review has vanished!")

            data = ns.payload.copy()
            data["user_id"] = review.user_id  # Empêcher le changement d'auteur

            updated_review = facade.update(Review, review_id, data)
            if not isinstance(updated_review, Review):
                ns.abort(400, "Failed to update the review!")
            return updated_review
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me(component="api")
    @ns.doc(
        "delete_review",
        responses={
            204: "Review deleted",
            400: "Invalid operation",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Review not found",
        },
    )
    @ns.param(
        "hard", "Perform hard delete (permanent)", type=bool, default=False
    )
    @admin_only
    def delete(self, review_id):
        """Banish a review from our realm! ⚡.

        Only administrators can delete reviews.
        Supports both soft and hard deletion.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            tuple: Empty response with 204 status code.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not an administrator.
            404: If the review doesn't exist.
            400: If the deletion fails."""
        review = facade.get(Review, review_id)
        if not isinstance(review, Review):
            ns.abort(404, "This review has already vanished!")

        hard = request.args.get("hard", "false").lower() == "true"
        try:
            facade.delete(Review, review_id, hard=hard)
            return "", 204
        except ValueError as e:
            ns.abort(400, str(e))
