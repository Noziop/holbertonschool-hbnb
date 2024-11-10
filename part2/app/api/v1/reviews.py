# app/api/v1/reviews.py
"""Where our beloved Haunted Spirit speaks to us! 🏚️"""

from app.api import log_me
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.services.facade import HBnBFacade
from flask import request
from flask_restx import Namespace, Resource, fields

ns = Namespace(
    "reviews",
    validate=True,
    description="Where our beloved Haunted Spirit speaks to us! 🏚️",
    path="/api/v1/reviews",
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


@ns.route("/")
class ReviewList(Resource):
    @log_me
    @ns.doc(
        "list_reviews",
        responses={200: "Success", 400: "Invalid parameters", 404: "No reviews found"},
    )
    @ns.marshal_list_with(output_review_model)
    @ns.param("user_id", "Ghost reviewer ID", type=str, required=False)
    @ns.param("place_id", "Haunted place ID", type=str, required=False)
    @ns.param("rating", "Spooky rating", type=int, required=False)
    def get(self):
        """List all haunted reviews! 👻"""
        try:
            criteria = {}
            for field in ["user_id", "place_id", "rating"]:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]
            return facade.find(Review, **criteria)
        except Exception as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @log_me
    @ns.doc(
        "create_review",
        responses={
            201: "Review created",
            400: "Invalid parameters",
            404: "User or Place not found",
        },
    )
    @ns.expect(input_review_model)
    @ns.marshal_with(output_review_model, code=201)
    def post(self):
        """Create a new haunted review! ✍️"""
        try:
            # Validate user and place existence
            facade.get(User, ns.payload["user_id"])
            facade.get(Place, ns.payload["place_id"])
            return facade.create(Review, ns.payload), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
@ns.param("review_id", "The haunted review identifier")
class ReviewDetail(Resource):
    @log_me
    @ns.doc("get_review", responses={200: "Success", 404: "Review not found"})
    @ns.marshal_with(output_review_model)
    def get(self, review_id):
        """Find a specific haunted review! 🔍"""
        try:
            review = facade.get(Review, review_id)
            if review.rating == None:
                ns.abort(404, "This review has vanished!")
            return review
        except ValueError:
            ns.abort(404, "This review has vanished!")

    @log_me
    @ns.doc(
        "update_review",
        responses={200: "Success", 400: "Invalid parameters", 404: "Review not found"},
    )
    @ns.expect(input_review_model)
    @ns.marshal_with(output_review_model)
    def put(self, review_id):
        """Update a haunted review! 📝"""
        try:
            return facade.update(Review, review_id, ns.payload)
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me
    @ns.doc(
        "delete_review",
        responses={
            204: "Review deleted",
            400: "Invalid operation",
            404: "Review not found",
        },
    )
    @ns.param("hard", "Perform hard delete (permanent)", type=bool, default=False)
    def delete(self, review_id):
        """Banish a review from our realm! ⚡"""
        try:
            # D'abord vérifier si la review existe
            review = facade.get(Review, review_id)
            if not review:
                ns.abort(404, "This review has already vanished!")

            hard = request.args.get("hard", "false").lower() == "true"
            try:
                facade.delete(Review, review_id, hard=hard)
                return "", 204
            except ValueError as e:
                # Si c'est une erreur de validation
                if "must be at least" in str(e):
                    ns.abort(400, str(e))
                raise  # Relancer l'erreur si c'est autre chose
        except ValueError as e:
            # Si la review n'existe pas
            ns.abort(404, "This review has vanished!")
