"""Where our beloved Haunted Spirit speaks to us! 🏚️."""

from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restx import Namespace, Resource, fields

from app.api import admin_only, auth_required, log_me, owner_only, user_only
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.services.facade import HBnBFacade

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter: **Bearer &lt;JWT&gt;**",
    },
}

ns = Namespace(
    "reviews",
    validate=True,
    description="Where our beloved Haunted Spirit speaks to us! 🏚️",
    authorizations=authorizations,
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
        "List all_reviews - Public endpoint",
        responses={
            200: "Success",
            400: "Invalid parameters",
        },
    )
    @ns.response(200, "Success", [output_review_model])
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

            # Retourner une liste vide avec 200 si pas de reviews
            return reviews or [], 200

        except Exception as e:
            return {
                "message": f"A spectral error occurred: {str(e)} 👻",
                "reviews": [],
            }, 400

    @log_me(component="api")
    @user_only
    @ns.doc(
        "Create a new review - Authenticated endpoint",
        security="Bearer Auth",
        responses={
            201: "Review created",
            400: "Invalid parameters",
            404: "User or Place not found",
            401: "Unauthorized",
            403: "Forbidden",
        },
    )
    @ns.expect(input_review_model)
    @ns.marshal_with(output_review_model, code=201)
    def post(self):
        """Create a new haunted review! ✍️"""
        try:
            from flask_jwt_extended import get_jwt

            claims = get_jwt()
            place = facade.get(Place, ns.payload["place_id"])
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            # Vérifier si l'utilisateur est le propriétaire
            if place.owner_id == claims["user_id"]:
                return {"message": "Cannot review your own place! 👻"}, 403

            # Créer la review
            review_data = {
                "user_id": claims["user_id"],
                "place_id": ns.payload["place_id"],
                "text": ns.payload["text"],
                "rating": ns.payload["rating"],
            }
            review = facade.create(Review, review_data)
            return review, 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
@ns.param("review_id", "The haunted review identifier")
class ReviewDetail(Resource):
    """Endpoint for managing individual haunted reviews! 👻"""

    @log_me(component="api")
    @ns.doc(
        "Get a specific review - Public endpoint",
        responses={200: "Success", 404: "Not Found"},
    )
    @ns.response(200, "Success", output_review_model)
    @ns.response(404, "Not Found", error_model)
    def get(self, review_id):
        """Find a specific haunted review! 🔍"""
        try:
            review = facade.get(Review, review_id)
            if not isinstance(review, Review) or review.rating is None:
                return {
                    "message": "This review has vanished! 👻",
                    "review": None,
                }, 404
            return review, 200
        except ValueError as e:
            return {
                "message": f"Failed to find review: {str(e)} 👻",
                "review": None,
            }, 404

    @log_me(component="api")
    @owner_only
    @ns.doc(
        "Update a review - Authenticated endpoint",
        security="Bearer Auth",
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
    def put(self, review_id):
        """Update a haunted review! 📝"""
        from flask_jwt_extended import get_jwt

        try:
            review = facade.get(Review, review_id)
            if not isinstance(review, Review):
                ns.abort(404, "This review has vanished!")

            claims = get_jwt()
            data = ns.payload.copy()
            data["user_id"] = review.user_id  # Empêcher le changement d'auteur

            updated_review = facade.update(
                Review,
                review_id,
                data,
                user_id=claims.get("user_id"),
                is_admin=claims.get("is_admin", False),
            )
            return updated_review
        except ValueError as e:
            ns.abort(403, str(e))

    @log_me(component="api")
    @owner_only  # On vérifie juste l'authentification
    @ns.doc(
        "Delete a review - Authenticated endpoint Admin only",
        security="Bearer Auth",
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
    def delete(self, review_id):
        """Banish a review from our realm! ⚡"""
        from flask_jwt_extended import get_jwt

        try:
            review = facade.get(Review, review_id)
            if not isinstance(review, Review):
                ns.abort(404, "This review has already vanished!")

            claims = get_jwt()
            hard = request.args.get("hard", "false").lower() == "true"

            facade.delete(
                Review,
                review_id,
                user_id=claims.get("user_id"),
                is_admin=claims.get("is_admin", False),
                hard=hard,
            )
            return "", 204
        except ValueError as e:
            ns.abort(403, str(e))
