"""Amenities API routes - The supernatural features catalog! 🎭."""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.api import admin_only, log_me
from app.models.amenity import Amenity
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
    "amenities",
    validate=True,
    description="Supernatural features operations 🎭",
    path="/api/v1/amenities",
    security="Bearer Auth",
)
facade = HBnBFacade()

# Modèles Swagger/OpenAPI
amenity_model = ns.model(
    "Amenity",
    {
        "id": fields.String(
            readonly=True,
            description="Unique feature identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "name": fields.String(
            required=True,
            min_length=3,
            description="Feature name",
            example="Ghost Detector",
        ),
        "description": fields.String(
            required=True,
            min_length=10,
            description="Feature description",
            example="Detects supernatural presence in the vicinity",
        ),
        "category": fields.String(
            required=False,
            enum=["safety", "comfort", "entertainment", "supernatural"],
            description="Feature category",
            example="supernatural",
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
class AmenityList(Resource):
    """Endpoint for managing supernatural features! 👻"""

    @log_me(component="api")
    @ns.doc(
        "List all amenities - Public",
        responses={
            200: "Success",
            400: "Invalid parameters",
        },
    )
    @ns.marshal_list_with(amenity_model)
    @ns.param("category", "Feature category", type=str, required=False)
    def get(self):
        """Browse our supernatural features catalog! 🎭"""
        try:
            criteria = {}
            if "category" in request.args:
                criteria["category"] = request.args["category"]
            amenities = facade.find(Amenity, **criteria)
            return amenities or [], 200
        except Exception as e:
            return {
                "message": f"A spectral error occurred: {str(e)} 👻",
                "amenities": [],
            }, 400

    @log_me(component="api")
    @admin_only
    @ns.doc(
        "Creata a new amenity - Admin only",
        security="Bearer Auth",
        responses={
            201: "Feature created",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Admin only",
        },
    )
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new supernatural feature! ✨"""
        try:
            amenity = facade.create(Amenity, ns.payload)
            return amenity, 201
        except Exception as e:
            return {
                "message": f"Failed to create feature: {str(e)} 👻",
                "amenity": None,
            }, 400


@ns.route("/<string:amenity_id>")
@ns.param("amenity_id", "The supernatural feature identifier")
class AmenityDetail(Resource):
    """Endpoint for managing individual features! 👻"""

    @log_me(component="api")
    @ns.doc(
        "Get a specific amenity details - Public Endpoint",
        responses={
            200: "Success",
            404: "Amenity not found",
        },
    )
    @ns.response(200, "Success", amenity_model)
    @ns.response(404, "Not Found", error_model)
    def get(self, amenity_id):
        """Find a specific supernatural feature! 🔍"""
        try:
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                return {
                    "message": "This feature has vanished! 👻",
                    "amenity": None,
                }, 404
            return amenity, 200
        except Exception as e:
            return {
                "message": f"Failed to find feature: {str(e)} 👻",
                "amenity": None,
            }, 404

    @log_me(component="api")
    @admin_only
    @ns.doc(
        "Update a feature - Admin only",
        security="Bearer Auth",
        responses={
            200: "Success",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Admin only",
            404: "Amenity not found",
        },
    )
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update a supernatural feature! 📝"""
        try:
            from flask_jwt_extended import get_jwt

            claims = get_jwt()
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This feature has vanished!")

            updated = facade.update(
                Amenity,
                amenity_id,
                ns.payload,
                user_id=claims.get("user_id"),
                is_admin=claims.get("is_admin", False),
            )
            return updated, 200
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me(component="api")
    @admin_only
    @ns.doc(
        "Delete a feature - Admin only",
        security="Bearer Auth",
        responses={
            204: "Amenity deleted",
            401: "Unauthorized",
            403: "Forbidden - Admin only",
            404: "Amenity not found",
        },
    )
    def delete(self, amenity_id):
        """Banish a feature from our realm! ⚡"""
        try:
            from flask_jwt_extended import get_jwt

            claims = get_jwt()
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This feature has vanished!")

            facade.delete(
                Amenity,
                amenity_id,
                user_id=claims.get("user_id"),
                is_admin=claims.get("is_admin", False),
                hard=True,
            )
            return "", 204
        except ValueError as e:
            ns.abort(400, str(e))


ns.route("/<string:amenity_id>/places")


@ns.param("amenity_id", "The supernatural feature identifier")
class AmenityPlaces(Resource):
    """Endpoint for listing places with specific features! 🏰.

    This endpoint allows retrieving all haunted places that have
    a specific supernatural feature installed."""

    @log_me(component="api")
    @ns.doc(
        "Get places with a specific amenity - Public endpoint",
        responses={200: "Success", 404: "Amenity not found"},
    )
    def get(self, amenity_id):
        """List all haunted places with this feature! 🏰.

        Args:
            amenity_id (str): The unique identifier of the feature.

        Returns:
            list[dict]: List of haunted places with this feature.

        Raises:
            404: If the feature doesn't exist."""
        amenity = facade.get(Amenity, amenity_id)
        if not isinstance(amenity, Amenity):
            ns.abort(404, "This feature has vanished!")

        return [place.to_dict() for place in amenity.get_places()]
