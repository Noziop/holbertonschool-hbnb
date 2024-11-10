"""Authentication endpoints for our haunted API! 👻."""

from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields

from app.models.user import User
from app.services.facade import HBnBFacade

ns = Namespace(
    "auth",
    validate=True,
    description="where keys can't help you, but ouija board does 🔐",
)

facade = HBnBFacade()

login_model = ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="Ghost's email 👻"),
        "password": fields.String(
            required=True, description="Ghost's secret spell 🔮"
        ),
    },
)


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    @ns.doc(
        "login",
        responses={
            200: "Welcome back, ghost! 👻",
            400: "Missing required fields! 🚫",
            401: "Invalid credentials! 💀",
            404: "User not found! 👻",
        },
    )
    def post(self):
        """Login and get a haunted token! 🎭."""
        data = request.get_json()

        # Vérifier que les données requises sont présentes
        if not data or not data.get("email") or not data.get("password"):
            return {
                "message": "The Ouija board needs both :"
                "email and password to work! 👻"
            }, 400

        user = facade.find(User, email=data.get("email"))
        if not user:
            return {
                "message": "This spirit is not registered in our realm! 👻"
            }, 404

        if not user.is_active:
            return {
                "message": "This spirit has been exorcised! 👻"
            }, 401

        if user.check_password(data.get("password")):
            token = create_access_token(
                identity=user.id,
                additional_claims={
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                },
            )
            return {
                    "message": "Welcome back to the spirit realm! 👻",
                    "token": token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "is_admin": user.is_admin,
                    },
                }, 200

        return {
                "message": "Wrong incantation! Try again, mortal! 💀"
            }, 401
