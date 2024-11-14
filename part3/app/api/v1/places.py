"""Places API routes - The haunted real estate office! 🏚️."""

from flask import request
from flask_jwt_extended import get_jwt
from flask_restx import Namespace, Resource, fields, reqparse

from app.api import admin_only, auth_required, log_me, owner_only, user_only
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity
from app.models.review import Review
from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "places", validate=True, description="Haunted property operations 👻"
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
class PlaceList(Resource):
    # Créer le parser pour les query parameters
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price_min", type=float, help="Minimum price per night"
    )
    parser.add_argument(
        "price_max", type=float, help="Maximum price per night"
    )
    parser.add_argument(
        "latitude", type=float, help="Latitude for location search"
    )
    parser.add_argument(
        "longitude", type=float, help="Longitude for location search"
    )
    parser.add_argument(
        "radius", type=float, default=10.0, help="Search radius in kilometers"
    )
    parser.add_argument(
        "amenities", type=str, action="append", help="Amenity IDs to filter by"
    )
    parser.add_argument(
        "property_type", type=str, help="Type of haunted property"
    )

    @log_me(component="api")
    @ns.doc(
        "list_places",
        responses={
            200: "Success",
            400: "Invalid parameters",
        },
    )
    @ns.expect(parser)  # Utiliser le parser
    @ns.marshal_list_with(place_model)
    def get(self):
        """Browse our haunted catalog! 👻"""
        try:
            args = self.parser.parse_args()

            # Vérifier les filtres de prix
            if args.price_min is not None and args.price_max is not None:
                places = Place.filter_by_price(args.price_min, args.price_max)
                return places or [], 200

            # Vérifier les filtres de localisation
            if args.latitude is not None and args.longitude is not None:
                # Valider les coordonnées
                if not (-90 <= args.latitude <= 90):
                    ns.abort(400, "Latitude must be between -90 and 90")
                if not (-180 <= args.longitude <= 180):
                    ns.abort(400, "Longitude must be between -180 and 180")

                places = Place.get_by_location(
                    args.latitude, args.longitude, args.radius
                )
                return places or [], 200

            # Vérifier les filtres d'équipements
            if args.amenities is not None:
                places = Place.find_by(Amenity, args.amenities)
                return places or [], 200

            if args.property_type is not None:
                places = Place.find_by(Place, args.property_type)
                return (places or [],)

            # Si pas de filtres, retourner toutes les places
            places = facade.find(Place)
            return places or [], 200

        except Exception as e:
            ns.abort(400, str(e))

    @log_me(component="api")
    @user_only
    @ns.doc(
        "create_place",
        responses={
            201: "Place created successfully",
            400: "Invalid input",
            401: "Unauthorized",
            403: "Forbidden - User not verified",
        },
    )
    @ns.expect(place_model)  # Validation après l'auth
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Summon a new haunted property! 🏗️"""
        try:
            place = facade.create(Place, ns.payload)
            if not isinstance(place, Place):
                return {
                    "message": "Failed to materialize the haunted property!",
                    "place": None,
                }, 400
            return place, 201
        except ValueError as e:
            return {
                "message": f"Invalid haunting parameters: {str(e)}",
                "place": None,
            }, 400


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
    @ns.doc("get_place")
    @ns.response(200, "Success", place_model)
    @ns.response(404, "Not Found", error_model)
    def get(self, place_id):
        try:
            place = facade.get(Place, place_id)
            return place, 200
        except ValueError:
            return {
                "message": "This ghost house has vanished! 👻",
                "place": None,
            }, 404

    @log_me(component="api")
    @owner_only
    @ns.doc(
        "update_place",
        responses={
            200: "Success",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Place not found",
        },
    )
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Renovate a haunted property! 🏚️"""
        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This ghost house has vanished!")

            claims = get_jwt()
            data = ns.payload.copy()
            data[
                "owner_id"
            ] = place.owner_id  # Empêcher le changement de propriétaire

            updated = facade.update(
                Place,
                place_id,
                data,
                user_id=claims.get("user_id"),
                is_admin=claims.get("is_admin", False),
            )
            return updated, 200
        except ValueError as e:
            ns.abort(403, str(e))

    @log_me(component="api")
    @owner_only
    @ns.doc(
        "delete_place",
        responses={
            204: "Place deleted",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Place not found",
        },
    )
    @ns.param(
        "hard", "Perform hard delete (permanent)", type=bool, default=False
    )
    def delete(self, place_id):
        """Exorcise a property! ⚡"""
        try:
            # Vérifier d'abord l'existence
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This ghost house has already vanished!")

            claims = get_jwt()
            hard = request.args.get("hard", "false").lower() == "true"

            # Ensuite tenter la suppression
            try:
                facade.delete(
                    Place,
                    place_id,
                    user_id=claims.get("user_id"),
                    is_admin=claims.get("is_admin", False),
                    hard=hard,
                )
                return "", 204
            except ValueError as e:
                ns.abort(403, str(e))
        except Exception as e:
            ns.abort(404, str(e))


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
    @owner_only  # On vérifie juste l'authentification
    @ns.doc(
        "add_amenity",
        responses={
            201: "Amenity added",
            400: "Invalid parameters",
            401: "Unauthorized",
            403: "Forbidden",
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
    def post(self, place_id):
        """Add a supernatural feature to a property! ✨"""
        try:
            claims = get_jwt()

            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            amenity_id = ns.payload["amenity_id"]
            amenity = facade.get(Amenity, amenity_id)
            if not isinstance(amenity, Amenity):
                ns.abort(404, "This supernatural feature doesn't exist!")
            try:
                link = facade.link_place_amenity(
                    place_id,
                    amenity_id,
                    user_id=claims.get("user_id"),
                    is_admin=claims.get("is_admin", False),
                )
                if not link:
                    ns.abort(
                        400, "Failed to install the supernatural feature!"
                    )
                return amenity, 201
            except ValueError as e:
                ns.abort(403, str(e))
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
    @user_only
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
        from flask_jwt_extended import get_jwt

        try:
            place = facade.get(Place, place_id)
            if not isinstance(place, Place):
                ns.abort(404, "This haunted property has vanished!")

            user = facade.get(User, ns.payload["user_id"])
            if not isinstance(user, User):
                ns.abort(404, "This ghost reviewer doesn't exist!")

            claims = get_jwt()
            if place.owner_id == claims["user_id"]:
                return {"message": "Cannot review your own place! 👻"}, 403

            # Créer la review
            review_data = {
                "user_id": claims["user_id"],
                "place_id": place_id,
                "text": ns.payload["text"],
                "rating": ns.payload["rating"],
            }
            review = facade.create(Review, review_data)
            return review, 201
        except ValueError as e:
            ns.abort(400, str(e))
