"""Places API routes - The haunted real estate office! 🏚️."""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.api import admin_only, auth_required, log_me, owner_only
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity
from app.models.review import Review
from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "places",
    validate=True,
    description="Haunted property operations 👻",
    path="/api/v1/places",
)
facade = HBnBFacade()

# Modèles Swagger/OpenAPI plus détaillés
place_model = ns.model(
    "Place",
    {
        "id": fields.String(
            readonly=True,
            description="Unique ghost identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "name": fields.String(
            required=True,
            min_length=3,
            description="Haunted house name",
            example="Spooky Manor",
        ),
        "description": fields.String(
            required=True,
            min_length=10,
            description="Ghost stories included",
            example="A very haunted place with mysterious occurrences",
        ),
        "number_rooms": fields.Integer(
            required=True, min=1, description="Haunted rooms count", example=5
        ),
        "number_bathrooms": fields.Integer(
            required=True, min=1, description="Possessed bathrooms", example=2
        ),
        "max_guest": fields.Integer(
            required=True,
            min=1,
            description="Maximum spirits allowed",
            example=4,
        ),
        "price_by_night": fields.Float(
            required=True,
            min=0.0,
            description="Price per haunted night",
            example=100.0,
        ),
        "latitude": fields.Float(
            required=False,
            min=-90.0,
            max=90.0,
            description="Supernatural latitude",
            example=45.5,
        ),
        "longitude": fields.Float(
            required=False,
            min=-180.0,
            max=180.0,
            description="Spectral longitude",
            example=-73.5,
        ),
        "owner_id": fields.String(
            required=True,
            description="Ghost owner ID",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "status": fields.String(
            required=False,
            enum=["active", "maintenance", "blocked"],
            description="Current haunting status",
            example="active",
        ),
        "property_type": fields.String(
            required=False,
            enum=["house", "apartment", "villa"],
            description="Type of haunted property",
            example="house",
        ),
    },
)

# Modèle pour les équipements surnaturels
place_amenity_model = ns.model(
    "PlaceAmenity",
    {
        "id": fields.String(
            readonly=True,
            description="Unique identifier for the supernatural feature.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "name": fields.String(
            required=True,
            description="Name of the supernatural feature.",
            example="Ghost Detector",
        ),
        "description": fields.String(
            required=True,
            description="Detailed description of "
            "the feature's supernatural properties.",
            example="Advanced EMF detector with "
            "spirit communication capabilities",
        ),
    },
)

# Modèle pour les avis spectraux
place_review_model = ns.model(
    "PlaceReview",
    {
        "id": fields.String(
            readonly=True,
            description="Unique identifier for the spectral review.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "user_id": fields.String(
            required=True,
            description="Identifier of the ghost who wrote the review.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "text": fields.String(
            required=True,
            min_length=10,
            description="The ghostly feedback about the property.",
            example="Perfect haunting spot! Great ambiance for spooking.",
        ),
        "rating": fields.Integer(
            required=True,
            min=1,
            max=5,
            description="Supernatural rating from 1 to 5 spirits.",
            example=5,
        ),
    },
)


@ns.route("/")
class PlaceList(Resource):
    """Endpoint for managing the collection of haunted properties! 👻.

    This endpoint handles listing all properties and creating new ones.
    Supports advanced filtering by price and location. Only authenticated
    users can create new properties."""

    @log_me(component="api")
    @ns.doc(
        "list_places",
        responses={
            200: "Success",
            400: "Invalid parameters",
            404: "No places found",
        },
    )
    @ns.marshal_list_with(place_model)
    @ns.param("price_min", "Minimum price per night", type=float)
    @ns.param("price_max", "Maximum price per night", type=float)
    @ns.param("latitude", "Latitude for location search", type=float)
    @ns.param("longitude", "Longitude for location search", type=float)
    @ns.param(
        "radius", "Search radius in kilometers", type=float, default=10.0
    )
    def get(self):
        """Browse our haunted catalog! 👻.

        Supports three search modes:
        1. Price range filtering
        2. Location-based search with customizable radius
        3. Complete catalog listing

        Returns:
            list[Place]: List of haunted properties matching the criteria.

        Raises:
            400: If the search parameters are invalid.
            404: If no properties are found."""
        try:
            # Filtrage par prix
            if "price_min" in request.args and "price_max" in request.args:
                min_price = float(request.args["price_min"])
                max_price = float(request.args["price_max"])
                places = Place.filter_by_price(min_price, max_price)
                if not places:
                    ns.abort(
                        404, "No haunted properties found in this price range!"
                    )
                return places

            # Recherche par localisation
            if all(k in request.args for k in ["latitude", "longitude"]):
                latitude = float(request.args["latitude"])
                longitude = float(request.args["longitude"])

                # Valider les coordonnées
                if not (-90 <= latitude <= 90):
                    raise ValueError("Latitude must be between -90 and 90")
                if not (-180 <= longitude <= 180):
                    raise ValueError("Longitude must be between -180 and 180")

                places = Place.get_by_location(
                    latitude,
                    longitude,
                    float(request.args.get("radius", 10.0)),
                )
                if not places:
                    ns.abort(404, "No haunted properties found in this area!")
                return places

            # Liste complète
            places = facade.find(Place)
            if not places:
                ns.abort(
                    404, "Our catalog seems to be haunted... by emptiness!"
                )
            return places

        except ValueError as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @log_me(component="api")
    @ns.doc(
        "create_place",
        responses={
            201: "Place created successfully",
            400: "Invalid input",
            401: "Unauthorized",
            403: "Forbidden - User not verified",
        },
    )
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    @auth_required()  # Seuls les utilisateurs authentifiés peuvent créer
    def post(self):
        """Summon a new haunted property! 🏗️.

        Only authenticated users can create new properties.
        The owner_id is automatically set to the authenticated user's ID.

        Returns:
            Place: The newly created haunted property.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not verified.
            400: If the property data is invalid."""
        try:
            place = facade.create(Place, ns.payload)
            if not isinstance(place, Place):
                ns.abort(400, "Failed to materialize the haunted property!")
            return place, 201
        except ValueError as e:
            ns.abort(400, f"Invalid haunting parameters: {str(e)}")


@ns.route("/<string:place_id>")
@ns.param("place_id", "The haunted property identifier")
class PlaceResource(Resource):
    """Endpoint for managing individual haunted properties! 👻.

    This endpoint handles :
    retrieving, updating, and deleting specific properties.
    Only owners can update their properties.
    admins can delete any property.
    """

    @log_me(component="api")
    @ns.doc("get_place", responses={200: "Success", 404: "Place not found"})
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Find a specific haunted house! 🔍.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            Place: The requested haunted property.

        Raises:
            404: If the property doesn't exist."""
        place = facade.get(Place, place_id)
        if not isinstance(place, Place):
            ns.abort(404, "This ghost house has vanished!")
        return place

    @log_me(component="api")
    @ns.doc(
        "update_place",
        responses={
            200: "Success",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Not the owner",
            404: "Place not found",
        },
    )
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    @owner_only  # Seul le propriétaire peut modifier
    def put(self, place_id):
        """Renovate a haunted property! 🏚️.

        Only the property owner can update their haunted house.
        The owner_id cannot be changed during update.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            Place: The updated haunted property.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not the owner.
            404: If the property doesn't exist.
            400: If the update data is invalid."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This ghost house has vanished!")

            data = ns.payload.copy()
            data[
                "owner_id"
            ] = place.owner_id  # Empêcher le changement de propriétaire

            updated = facade.update(Place, place_id, data)
            if not isinstance(updated, Place):
                ns.abort(400, "Failed to renovate the haunted property!")
            return updated
        except ValueError as e:
            ns.abort(400, f"Invalid renovation plans: {str(e)}")

    @log_me(component="api")
    @ns.doc(
        "delete_place",
        responses={
            204: "Place deleted",
            401: "Unauthorized",
            403: "Forbidden - Admin only",
            404: "Place not found",
        },
    )
    @ns.param(
        "hard", "Perform hard delete (permanent)", type=bool, default=False
    )
    @ns.response(204, "Ghost house vanished")
    @admin_only  # Seul l'admin peut supprimer
    def delete(self, place_id):
        """Exorcise a property! ⚡.

        Only administrators can delete properties.
        Supports both soft and hard deletion.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            tuple: Empty response with 204 status code.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not an administrator.
            404: If the property doesn't exist.
            400: If the deletion fails."""
        place = facade.get(Place, place_id)
        if not isinstance(place, Place):
            ns.abort(404, "This ghost house has already vanished!")

        try:
            hard = request.args.get("hard", "false").lower() == "true"
            facade.delete(Place, place_id, hard=hard)
            return "", 204
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:place_id>/amenities")
@ns.param("place_id", "The haunted property identifier")
class PlaceAmenities(Resource):
    """Endpoint for managing supernatural features of a haunted property! 👻.

    This endpoint handles :
    listing and adding supernatural features to a property.
    Only property owners can add new features to their properties."""

    @log_me(component="api")
    @ns.doc(
        "get_place_amenities",
        responses={200: "Success", 404: "Place not found"},
    )
    @ns.marshal_list_with(place_amenity_model)
    def get(self, place_id):
        """Get all supernatural features of a property! 👻.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            list[Amenity]: List of supernatural features
                            installed in the property.

        Raises:
            404: If the property doesn't exist."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            links = facade.find(PlaceAmenity, place_id=place_id)
            amenities = []
            for link in links:
                amenity = facade.get(Amenity, link.amenity_id)
                if isinstance(amenity, Amenity):
                    amenities.append(amenity)

            return amenities
        except ValueError as e:
            ns.abort(404, str(e))

    @log_me(component="api")
    @ns.doc(
        "add_amenity",
        responses={
            201: "Amenity added",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Not the owner",
            404: "Place or Amenity not found",
        },
    )
    @ns.expect(
        ns.model(
            "AmenityId",
            {
                "amenity_id": fields.String(
                    required=True,
                    description="The supernatural feature ID",
                    example="123e4567-e89b-12d3-a456-426614174000",
                )
            },
        )
    )
    @ns.marshal_with(place_amenity_model, code=201)
    @owner_only  # Seul le propriétaire peut ajouter des équipements
    def post(self, place_id):
        """Add a supernatural feature to a property! ✨.

        Only the property owner can add features.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            Amenity: The added supernatural feature.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not the property owner.
            404: If the property or feature doesn't exist.
            400: If the feature cannot be added."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            amenity_id = ns.payload["amenity_id"]
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This supernatural feature doesn't exist!")

            if facade.link_place_amenity(place_id, amenity_id):
                return amenity, 201
            ns.abort(400, "Failed to install the supernatural feature!")
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:place_id>/amenities/<string:amenity_id>")
@ns.param("place_id", "The haunted place identifier")
@ns.param("amenity_id", "The supernatural feature identifier")
class PlaceAmenityLink(Resource):
    """Endpoint for managing individual feature links to properties! 👻.

    This endpoint handles linking specific supernatural features to properties.
    Only property owners can add features to their properties."""

    @log_me(component="api")
    @ns.doc(
        "link_amenity",
        responses={
            201: "Amenity linked",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Not the owner",
            404: "Place or Amenity not found",
        },
    )
    @owner_only  # Seul le propriétaire peut ajouter des équipements
    def post(self, place_id, amenity_id):
        """Add a supernatural feature to a place! ✨.

        Only the property owner can add features.

        Args:
            place_id (str): The unique identifier of the haunted property.
            amenity_id (str): The unique identifier
                                of the supernatural feature.

        Returns:
            tuple: Empty response with 201 status code.

        Raises:
            401: If the user is not authenticated.
            403: If the user is not the property owner.
            404: If the property or feature doesn't exist.
            400: If the feature cannot be added."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This supernatural feature doesn't exist!")

            if facade.link_place_amenity(place_id, amenity_id):
                return "", 201
            ns.abort(400, "Failed to install the supernatural feature!")
        except ValueError as e:
            ns.abort(404, str(e))


@ns.route("/<string:place_id>/reviews")
@ns.param("place_id", "The haunted property identifier")
class PlaceReviews(Resource):
    """Endpoint for managing reviews of a haunted property! 📖.

    This endpoint handles listing and adding spectral reviews to a property.
    Only authenticated users who have stayed at the property can add reviews.
    """

    @log_me(component="api")
    @ns.doc(
        "get_place_reviews", responses={200: "Success", 404: "Place not found"}
    )
    @ns.marshal_list_with(place_review_model)
    def get(self, place_id):
        """Read the ghostly guestbook! 📖.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            list[Review]: List of spectral reviews for the property.

        Raises:
            404: If the property doesn't exist."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            reviews = facade.find(Review, place_id=place_id)
            return [r for r in reviews if isinstance(r, Review)]
        except ValueError as e:
            ns.abort(404, str(e))

    @log_me(component="api")
    @ns.doc(
        "add_review",
        responses={
            201: "Review added",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden - Not a verified guest",
            404: "Place or User not found",
        },
    )
    @ns.expect(place_review_model)
    @ns.marshal_with(place_review_model, code=201)
    @auth_required()  # Seuls les utilisateurs authentifiés peuvent poster
    def post(self, place_id):
        """Add a haunted experience! ✍️.

        Only authenticated users can add reviews.
        The user must have stayed at the property to review it.

        Args:
            place_id (str): The unique identifier of the haunted property.

        Returns:
            Review: The newly created spectral review.

        Raises:
            401: If the user is not authenticated.
            403: If the user hasn't stayed at the property.
            404: If the property doesn't exist.
            400: If the review data is invalid."""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            user = facade.get(User, ns.payload["user_id"])
            if not isinstance(user, User):
                ns.abort(404, "This ghost reviewer doesn't exist!")

            review_data = {**ns.payload, "place_id": place_id}
            review = facade.create(Review, review_data)

            if not isinstance(review, Review):
                ns.abort(400, "Failed to materialize the review!")
            return review, 201
        except ValueError as e:
            ns.abort(400, str(e))
