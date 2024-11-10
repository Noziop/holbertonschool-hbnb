"""User management endpoints for our haunted API! 👻."""

from flask import request
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
    """Endpoint for managing the collection of spectral users! 👻.

    This endpoint handles listing all users and creating new ones.
    Only administrators can create new users, but anyone can view
    the list of active spirits."""

    @log_me(component="api")
    @ns.doc(
        "list_users",
        responses={
            200: "Success - List of spirits returned",
            400: "Invalid parameters - Malformed search criteria",
            401: "Unauthorized - Authentication required",
            404: "No spirits found in the ethereal plane",
        },
    )
    @ns.marshal_list_with(output_user_model)
    @ns.param("username", "Ghost name", type=str, required=False)
    @ns.param("email", "Spirit contact", type=str, required=False)
    @ns.param("first_name", "First haunting name", type=str, required=False)
    @ns.param("last_name", "Last haunting name", type=str, required=False)
    @auth_required()  # Authenticated users only
    def get(self):
        """Browse Lilith's List of Lost Souls! 📖.

        Search through our spectral directory with various filters.
        Only active spirits are shown to protect the privacy of the departed.

        Returns:
            list[User]: List of spectral users matching the search criteria.

        Raises:
            401: If the requester is not authenticated.
            400: If the search parameters are invalid.
            404: If no spirits match the criteria."""
        try:
            criteria = {}
            for field in ["username", "email", "first_name", "last_name"]:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]

            users = facade.find(User, **criteria)
            if not users:
                ns.abort(404, "No spirits found in this realm! 👻")

            # Ne retourner que les utilisateurs actifs
            return [
                user
                for user in users
                if isinstance(user, User) and user.is_active
            ]
        except ValueError as e:
            ns.abort(400, f"Invalid summoning parameters: {str(e)}")

    @log_me(component="api")
    @ns.doc(
        "create_user",
        responses={
            201: "Spirit successfully summoned",
            400: "Invalid summoning parameters",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Admin privileges required",
        },
    )
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=201)
    @admin_only  # Seuls les admins peuvent créer des utilisateurs
    def post(self):
        """Summon a new lost soul to our realm! 🌟.

        Only Head Ghosts (administrators) can perform this ritual.
        New spirits are created with default mortal privileges.

        Returns:
            User: The newly summoned spectral entity.

        Raises:
            401: If the summoner is not authenticated.
            403: If the summoner lacks Head Ghost privileges.
            400: If the summoning parameters are invalid."""
        try:
            user = facade.create(User, ns.payload)
            if not isinstance(user, User):
                ns.abort(400, "The summoning ritual failed! 👻")
            return user, 201
        except ValueError as e:
            ns.abort(400, f"Invalid summoning parameters: {str(e)}")


@ns.route("/<string:user_id>")
@ns.param("user_id", "Spectral identifier")
class UserDetail(Resource):
    """Endpoint for managing individual spectral entities! 👻.

    This endpoint handles retrieving, updating, and banishing specific spirits.
    Users can only modify their own data.
    Administrators can manage all spirits.
    """

    @log_me(component="api")
    @ns.doc(
        "get_user",
        responses={
            200: "Spirit successfully contacted",
            401: "Unauthorized - Authentication required",
            404: "Spirit not found in this realm",
        },
    )
    @ns.marshal_with(output_user_model, code=200)
    @auth_required()  # Authentification requise
    def get(self, user_id):
        """Contact a specific spirit in our realm! 👻.

        Args:
            user_id (str): The unique identifier of the spirit.

        Returns:
            User: The requested spectral entity.

        Raises:
            401: If the requester is not authenticated.
            404: If the spirit doesn't exist."""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                ns.abort(404, "This spirit has crossed over! 👻")
            return user
        except ValueError as e:
            ns.abort(404, f"Spirit not found: {str(e)}")

    @log_me(component="api")
    @ns.doc(
        "update_user",
        responses={
            200: "Spirit successfully updated",
            400: "Invalid modification parameters",
            401: "Unauthorized - Authentication required",
            403: "Forbidden - Not your spiritual essence",
            404: "Spirit not found in this realm",
        },
    )
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=200)
    @owner_only  # Seul le propriétaire ou un admin peut modifier
    def put(self, user_id):
        """Modify a spirit's ethereal essence! ✨.

        Only the spirit itself or a Head Ghost can perform modifications.
        Some attributes can only be modified by Head Ghosts.

        Args:
            user_id (str): The unique identifier of the spirit.

        Returns:
            User: The updated spectral entity.

        Raises:
            401: If the requester is not authenticated.
            403: If the requester lacks proper permissions.
            404: If the spirit doesn't exist.
            400: If the modification parameters are invalid."""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                ns.abort(404, "This spirit has crossed over! 👻")

            data = ns.payload.copy()
            # Seuls les admins peuvent modifier ces champs
            if not user.is_admin:
                data.pop("is_admin", None)
                data.pop("is_active", None)

            updated = facade.update(User, user_id, data)
            if not isinstance(updated, User):
                ns.abort(400, "Failed to modify the spirit! 👻")
            return updated
        except ValueError as e:
            ns.abort(400, f"Invalid modification parameters: {str(e)}")

    @log_me(component="api")
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
    @admin_only  # Seuls les admins peuvent supprimer
    def delete(self, user_id):
        """Banish a spirit from our realm! ⚡.

        Only Head Ghosts can perform banishments.
        Supports both temporary (soft) and permanent (hard) banishments.

        Args:
            user_id (str): The unique identifier of the spirit.

        Returns:
            tuple: Empty response with 204 status code.

        Raises:
            401: If the requester is not authenticated.
            403: If the requester is not a Head Ghost.
            404: If the spirit doesn't exist."""
        try:
            user = facade.get(User, user_id)
            if not isinstance(user, User):
                ns.abort(404, "This spirit has already crossed over! 👻")

            hard = request.args.get("hard", "false").lower() == "true"
            if facade.delete(User, user_id, hard=hard):
                return "", 204
            ns.abort(400, "Failed to banish the spirit! 👻")
        except ValueError as e:
            ns.abort(404, f"Spirit not found: {str(e)}")
