"""Amenities API routes - The supernatural features catalog! 🎭."""

from flask_restx import Namespace, Resource, fields
from flask import request

from app.api import log_me, admin_only
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade

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
    """Endpoint for managing the collection of supernatural features! 👻.
    
    This endpoint handles listing all amenities and creating new ones.
    Only administrators can create new features, but anyone can view them.
    Supports filtering by category."""

    @log_me(component="api")
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
        """Browse our supernatural features catalog! 🎭.
        
        Supports filtering by category (safety, comfort, entertainment, supernatural).
        
        Returns:
            list[Amenity]: List of supernatural features matching the criteria.
            
        Raises:
            404: If no features are found.
            400: If the filter parameters are invalid."""
        try:
            criteria = {}
            if "category" in request.args:
                criteria["category"] = request.args["category"]
            amenities = facade.find(Amenity, **criteria)
            if not amenities:
                ns.abort(404, "No supernatural features found!")
            return amenities
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me(component="api")
    @ns.doc(
        "create_amenity",
        responses={
            201: "Amenity created", 
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Admin only"
        },
    )
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    @admin_only
    def post(self):
        """Add a new supernatural feature! ✨.
        
        Only administrators can create new features.
        
        Returns:
            Amenity: The newly created supernatural feature.
            
        Raises:
            401: If the user is not authenticated.
            403: If the user is not an administrator.
            400: If the feature data is invalid."""
        try:
            amenity = facade.create(Amenity, ns.payload)
            if not isinstance(amenity, Amenity):
                ns.abort(400, "Failed to materialize the feature!")
            return amenity, 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:amenity_id>")
@ns.param("amenity_id", "The supernatural feature identifier")
class AmenityDetail(Resource):
    """Endpoint for managing individual supernatural features! 👻.
    
    This endpoint handles retrieving, updating, and deleting specific features.
    Only administrators can modify or delete features, but anyone can view them."""

    @log_me(component="api")
    @ns.doc(
        "get_amenity", 
        responses={200: "Success", 404: "Amenity not found"}
    )
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Find a specific supernatural feature! 🔍.
        
        Args:
            amenity_id (str): The unique identifier of the feature.
            
        Returns:
            Amenity: The requested supernatural feature.
            
        Raises:
            404: If the feature doesn't exist."""
        amenity = facade.get(Amenity, amenity_id)
        if not isinstance(amenity, Amenity):
            ns.abort(404, "This feature has vanished!")
        return amenity

    @log_me(component="api")
    @ns.doc(
        "update_amenity",
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
    @admin_only
    def put(self, amenity_id):
        """Update a supernatural feature! 📝.
        
        Only administrators can update features.
        
        Args:
            amenity_id (str): The unique identifier of the feature.
            
        Returns:
            Amenity: The updated supernatural feature.
            
        Raises:
            401: If the user is not authenticated.
            403: If the user is not an administrator.
            404: If the feature doesn't exist.
            400: If the update data is invalid."""
        try:
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This feature has vanished!")
            
            updated = facade.update(Amenity, amenity_id, ns.payload)
            if not isinstance(updated, Amenity):
                ns.abort(400, "Failed to update the feature!")
            return updated
        except ValueError as e:
            ns.abort(400, str(e))

    @log_me(component="api")
    @ns.doc(
        "delete_amenity",
        responses={
            204: "Amenity deleted", 
            401: "Unauthorized",
            403: "Forbidden - Admin only",
            404: "Amenity not found"
        },
    )
    @admin_only
    def delete(self, amenity_id):
        """Banish a feature from our realm! ⚡.
        
        Only administrators can delete features.
        All deletions are permanent (hard delete).
        
        Args:
            amenity_id (str): The unique identifier of the feature.
            
        Returns:
            tuple: Empty response with 204 status code.
            
        Raises:
            401: If the user is not authenticated.
            403: If the user is not an administrator.
            404: If the feature doesn't exist.
            400: If the deletion fails."""
        amenity = facade.get(Amenity, amenity_id)
        if not isinstance(amenity, Amenity):
            ns.abort(404, "This feature has vanished!")
            
        try:
            facade.delete(Amenity, amenity_id, hard=True)
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
        "get_amenity_places",
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
    