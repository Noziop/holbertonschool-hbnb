"""User management endpoints for our haunted API! 👻."""

from flask import request
from flask_jwt_extended import get_jwt
from flask_restx import Namespace, Resource, fields

from app.api import admin_only, auth_required, log_me, owner_only
from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "users",
    validate=True,
    description="Where lost souls come to REST! 👻",
    path="api/v1/users",
)
facade = HBnBFacade()

# Modèle pour la création et mise à jour des utilisateurs
user_model = ns.model(
    "User",
    {
        "id": fields.String(
            readonly=True,
            description="Unique spectral identifier for eternal recognition.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "username": fields.String(
            required=True,
            description="Unique ghostly username "
            "(3-30 characters, letters, numbers, _ or -).",
            example="Casper_The_Friendly",
            min_length=3,
            max_length=30,
        ),
        "email": fields.String(
            required=True,
            description="Ethereal email address for spectral communications.",
            example="casper@haunted.ghost",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
        "password": fields.String(
            required=True,
            description="Secret incantation "
            "(min 8 chars, 1 upper, 1 lower, 1 number).",
            example="Boo_123!",
            min_length=8,
        ),
        "first_name": fields.String(
            required=True,
            description="First ethereal name.",
            example="Casper",
            min_length=2,
        ),
        "last_name": fields.String(
            required=True,
            description="Family spirit name.",
            example="The_Friendly_Ghost",
            min_length=2,
        ),
        "phone_number": fields.String(
            description="Spectral communication device number.",
            example="+666-666-6666",
            pattern=r"^\+?[0-9\-]{10,15}$",
        ),
        "address": fields.String(
            description="Location of haunting residence.",
            example="666 Haunted Manor Lane",
        ),
        "postal_code": fields.String(
            description="Ethereal postal routing code.",
            example="H4UN7",
        ),
        "city": fields.String(
            description="Metropolitan haunting grounds.",
            example="Ghostly Heights",
        ),
        "country": fields.String(
            description="Sovereign spectral territory.",
            example="Paranormal Republic",
        ),
        "is_active": fields.Boolean(
            required=True,
            description="Spirit manifestation status.",
            default=True,
        ),
    },
)

# Modèle pour les réponses (sans données sensibles)
output_user_model = ns.model(
    "User_output",
    {
        "id": fields.String(
            readonly=True,
            description="Unique spectral identifier for eternal recognition.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "username": fields.String(
            required=True,
            description="Unique ghostly username.",
            example="Casper_The_Friendly",
        ),
        "email": fields.String(
            required=True,
            description="Ethereal email address.",
            example="casper@haunted.ghost",
        ),
        "first_name": fields.String(
            required=True,
            description="First ethereal name.",
            example="Casper",
        ),
        "last_name": fields.String(
            required=True,
            description="Family spirit name.",
            example="The_Friendly_Ghost",
        ),
        "phone_number": fields.String(
            description="Spectral communication device number.",
            example="+666-666-6666",
        ),
        "address": fields.String(
            description="Location of haunting residence.",
            example="666 Haunted Manor Lane",
        ),
        "postal_code": fields.String(
            description="Ethereal postal routing code.",
            example="H4UN7",
        ),
        "city": fields.String(
            description="Metropolitan haunting grounds.",
            example="Ghostly Heights",
        ),
        "country": fields.String(
            description="Sovereign spectral territory.",
            example="Paranormal Republic",
        ),
        "is_active": fields.Boolean(
            required=True,
            description="Spirit manifestation status.",
        ),
        "is_admin": fields.Boolean(
            required=True,
            readonly=True,
            description="Head Ghost privileges.",
            default=False,
        ),
    },
)


# Winding Routes 🛤️ to the realm of Haunted BnB
@ns.route("/")
class UserList(Resource):
    """Endpoint for managing the collection of spectral users! 👻"""

    @log_me(component="api")
    @admin_only  #
    @ns.doc(
        "list_users",
        responses={
            200: "Success - List of spirits returned",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Admin privileges required",
            404: "No spirits found in the ethereal plane",
        },
    )
    @ns.marshal_list_with(output_user_model)
    @ns.param("username", "Ghost name", type=str, required=False)
    @ns.param("email", "Spirit contact", type=str, required=False)
    @ns.param("first_name", "First haunting name", type=str, required=False)
    @ns.param("last_name", "Last haunting name", type=str, required=False)
    def get(self):
        """Browse Lilith's List of Lost Souls! 📖"""
        try:
            criteria = {}
            for field in ["username", "email", "first_name", "last_name"]:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]

            users = facade.find(User, **criteria)

            # Retourner une liste vide si pas d'utilisateurs
            if not users:
                return [], 200

            # Filtrer les utilisateurs actifs
            return [user for user in users if user.is_active], 200

        except Exception as e:
            return {"message": str(e)}, 400

    @log_me(component="api")
    @admin_only
    @ns.doc(
        "create_user",
        responses={
            201: "Spirit successfully summoned",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Admin privileges required",
            400: "Invalid summoning parameters",
        },
    )
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=201)
    def post(self):
        """Summon a new lost soul to our realm! 🌟."""
        try:
            user = facade.create(User, ns.payload)
            return user, 201
        except ValueError as e:
            return {"message": str(e)}, 400


@ns.route("/<string:user_id>")
@ns.param("user_id", "Spectral identifier")
class UserDetail(Resource):
    """Endpoint for managing individual spectral entities! 👻"""

    @log_me(component="api")
    @auth_required()
    @ns.doc(
        "get_user",
        responses={
            200: "Spirit successfully contacted",
            401: "Unauthorized - Authentication required",
            404: "Spirit not found in this realm",
        },
    )
    @ns.marshal_with(output_user_model, code=200)
    def get(self, user_id):
        """Contact a specific spirit in our realm! 👻"""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                return {
                    "message": "This spirit has crossed over! 👻",
                    "user": None,
                }, 404
            return user, 200
        except Exception as e:
            return {
                "message": f"Spirit not found: {str(e)} 👻",
                "user": None,
            }, 404

    @log_me(component="api")
    @owner_only  # Vérifie auth + propriété/admin
    @ns.doc(...)
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=200)
    def put(self, user_id):
        """Modify a spirit's ethereal essence! ✨"""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                return {
                    "message": "This spirit has crossed over! 👻",
                    "user": None,
                }, 404

            data = ns.payload.copy()
            claims = get_jwt()

            # Si pas admin, on ne peut pas modifier certains champs
            if not claims.get("is_admin"):
                data.pop("is_admin", None)
                data.pop("is_active", None)
                # Le reste est modifiable par le propriétaire
            # Si admin, tout est modifiable !

            updated = facade.update(User, user_id, data)
            return updated, 200
        except ValueError as e:
            return {
                "message": f"Invalid modification parameters: {str(e)} 👻",
                "user": None,
            }, 400

    @log_me(component="api")
    @admin_only
    @ns.doc(
        "delete_user",
        responses={
            204: "Spirit successfully banished",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Admin privileges required",
            404: "Spirit not found in this realm",
        },
    )
    @ns.param(
        "hard",
        "Perform permanent exorcism (no return possible)",
        type=bool,
        default=False,
    )
    def delete(self, user_id):
        """Banish a spirit from our realm! ⚡"""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                return {
                    "message": "This spirit has already crossed over! 👻"
                }, 404

            hard = request.args.get("hard", "false").lower() == "true"
            if facade.delete(User, user_id, hard=hard):
                return "", 204
            return {"message": "Failed to banish the spirit! 👻"}, 400
        except ValueError as e:
            return {"message": f"Spirit not found: {str(e)} 👻"}, 404
