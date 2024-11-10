# app/api/v1/users.py
"""Where ghost haunts and REST! 🏚️"""

from flask import request
from flask_restx import Namespace, Resource, fields

from app.api import log_me
from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "users",
    validate=True,
    description="Where lost souls come to REST! 👻",
    path="api/v1/users",
)
facade = HBnBFacade()


# Book of Spells 📖 Tell us your deepest Secrets!
user_model = ns.model(
    "User",
    {
        "id": fields.String(
            readonly=True,
            description="Spectral identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "username": fields.String(
            required=True, description="Ghost name", example="Casper"
        ),
        "email": fields.String(
            required=True,
            description="Spirit contact",
            example="caspe@lost-souls.ghost",
        ),
        "password": fields.String(
            required=True,
            description="Supernatural secret",
            example="IcyD34dPe0p!e",
        ),
        "first_name": fields.String(
            required=True, description="First haunting name", example="Casper"
        ),
        "last_name": fields.String(
            required=True,
            description="Last haunting name",
            example="The Friendly_Ghost",
        ),
        "phone_number": fields.String(
            description="Ghostly phone", example="+666666666"
        ),
        "address": fields.String(
            description="Haunting address", example="123 Ghostly Lane"
        ),
        "postal_code": fields.String(
            description="Spectral code", example="66666"
        ),
        "city": fields.String(
            description="City of haunting", example="Ghostly Town"
        ),
        "country": fields.String(
            description="Realm of existence", example="Ghostly Realm"
        ),
        "is_active": fields.Boolean(
            required=True, description="Is the ghost active?", default=True
        ),
    },
)

# Book of Shadows 📖 The spirits that haunt us! but we won't reveal your secrets !
output_user_model = ns.model(
    "User_output",
    {
        "id": fields.String(
            readonly=True,
            description="Spectral identifier",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
        "username": fields.String(
            required=True, description="Ghost name", example="Casper"
        ),
        "email": fields.String(
            required=True,
            description="Spirit contact",
            example="casper@lost-souls.ghost",
        ),
        "first_name": fields.String(
            required=True, description="First haunting name", example="Casper"
        ),
        "last_name": fields.String(
            required=True,
            description="Last haunting name",
            example="The Friendly_Ghost",
        ),
        "phone_number": fields.String(
            description="Ghostly phone", example="+666666666"
        ),
        "address": fields.String(
            description="Haunting address", example="123 Ghostly Lane"
        ),
        "postal_code": fields.String(
            description="Spectral code", example="66666"
        ),
        "city": fields.String(
            description="City of haunting", example="Ghostly Town"
        ),
        "country": fields.String(
            description="Realm of existence", example="Ghostly Realm"
        ),
        "is_active": fields.Boolean(
            required=True, description="Is the ghost active?"
        ),
        "is_admin": fields.Boolean(
            required=True,
            readonly=True,
            description="Is the ghost an admin?",
            default=False,
        ),
    },
)


# Winding Routes 🛤️ to the realm of Haunted BnB
@ns.route("/")
class UserList(Resource):
    @log_me
    @ns.doc(
        "list_users",
        responses={
            200: "Success",
            400: "Invalid parameters",
            404: "No users found",
        },
    )
    @ns.marshal_list_with(output_user_model)
    @ns.param("username", "Ghost name", type=str, required=False)
    @ns.param("email", "Spirit contact", type=str, required=False)
    @ns.param("first_name", "First haunting name", type=str, required=False)
    @ns.param("last_name", "Last haunting name", type=str, required=False)
    def get(self):
        """Lilith's List of Lost Souls"""
        try:
            criteria = {}
            for field in ["username", "email", "first_name", "last_name"]:
                if field in request.args and request.args[field]:
                    criteria[field] = request.args[field]
            return facade.find(User, **criteria)
        except Exception as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @log_me
    @ns.doc(
        "create_user",
        responses={
            201: "Success",
            400: "Invalid parameters",
            401: "Unauthorized",
        },
    )
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=201)
    def post(self):
        """Summon a new lost soul"""
        try:
            return facade.create(User, ns.payload), 201
        except Exception as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")


@ns.route("/<string:user_id>")
@ns.param("user_id", "Spectral identifier")
class UserDetail(Resource):
    @log_me
    @ns.doc("get_user", responses={200: "Success", 404: "User not found"})
    @ns.marshal_with(output_user_model, code=200)
    def get(self, user_id):
        """Find a specific lost soul"""
        try:
            return facade.get(User, user_id)
        except Exception as e:
            ns.abort(404, f"User not found: {str(e)}")

    @log_me
    @ns.doc(
        "update_user",
        responses={
            200: "Success",
            400: "Invalid parameters",
            404: "User not found",
        },
    )
    @ns.expect(user_model)
    @ns.marshal_with(output_user_model, code=200)
    def put(self, user_id):
        """Update a lost soul"""
        try:
            return facade.update(User, user_id, ns.payload)
        except Exception as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @log_me
    @ns.doc("delete_user", responses={204: "Success", 404: "User not found"})
    @ns.param(
        "hard", "Perform hard delete (permanent)", type=bool, default=False
    )
    def delete(self, user_id):
        """Release a lost soul"""
        try:
            hard = request.args.get("hard", "false").lower() == "true"
            facade.delete(User, user_id, hard=hard)
            return "", 204
        except Exception as e:
            ns.abort(404, f"User not found: {str(e)}")
