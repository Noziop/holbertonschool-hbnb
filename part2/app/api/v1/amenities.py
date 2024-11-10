# app/api/v1/amenities.py
"""Amenities API routes - The supernatural features catalog! 🎭"""

from app.api import log_me
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade
from flask import request
from flask_restx import Namespace, Resource, fields

ns = Namespace(
    "amenities",
    validate=True,
    description="Supernatural features operations 🎭",
    path="/api/v1/amenities",
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


@ns.route("/")
class AmenityList(Resource):
    @log_me
    @ns.doc(
        "list_amenities",
        responses={
            200: "Success",
            400: "Invalid parameters",
            404: "No amenities found",
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
            return facade.find(Amenity, **criteria)
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me
    @ns.doc(
        "create_amenity", responses={201: "Amenity created", 400: "Invalid parameters"}
    )
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Add a new supernatural feature! ✨"""
        try:
            return facade.create(Amenity, ns.payload), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:amenity_id>")
@ns.param("amenity_id", "The supernatural feature identifier")
class AmenityDetail(Resource):
    @log_me
    @ns.doc("get_amenity", responses={200: "Success", 404: "Amenity not found"})
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Find a specific supernatural feature! 🔍"""
        try:
            return facade.get(Amenity, amenity_id)
        except ValueError:
            ns.abort(404, "This feature has vanished!")

    @log_me
    @ns.doc(
        "update_amenity",
        responses={200: "Success", 400: "Invalid parameters", 404: "Amenity not found"},
    )
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update a supernatural feature! 📝"""
        try:
            return facade.update(Amenity, amenity_id, ns.payload)
        except ValueError as e:
            if "not found" in str(e):
                ns.abort(404, str(e))
            ns.abort(400, str(e))

    @log_me
    @ns.doc(
        "delete_amenity", responses={204: "Amenity deleted", 404: "Amenity not found"}
    )
    def delete(self, amenity_id):
        """Banish a feature from our realm! ⚡"""
        try:
            facade.delete(Amenity, amenity_id, hard=True)  # always hard delete
            return "", 204
        except ValueError as e:
            ns.abort(404, str(e))


@ns.route("/<string:amenity_id>/places")
@ns.param("amenity_id", "The supernatural feature identifier")
class AmenityPlaces(Resource):
    @log_me
    @ns.doc("get_amenity_places", responses={200: "Success", 404: "Amenity not found"})
    def get(self, amenity_id):
        """List all haunted places with this feature! 🏰"""
        try:
            # Vérifie que l'amenity existe
            amenity = facade.get(Amenity, amenity_id)
            return [place.to_dict() for place in amenity.get_places()]
        except ValueError as e:
            ns.abort(404, str(e))
