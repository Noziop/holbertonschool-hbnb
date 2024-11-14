"""Authentication endpoints for our haunted API! 👻."""

from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Namespace, Resource, fields

from app.models.user import User
from app.services.facade import HBnBFacade
from app.utils import log_me

ns = Namespace(
    "login",
    validate=True,
    description="Where keys can't help you, but ouija board does 🔐.",
)

facade = HBnBFacade()

login_model = ns.model(
    "Login",
    {
        "email": fields.String(
            required=True,
            description="Ghost's email address for identification.",
            example="casper@haunted.com",
        ),
        "password": fields.String(
            required=True,
            description="Ghost's secret spell for authentication.",
            example="Boo_123!",
        ),
    },
)


@ns.route("/")
class Login(Resource):
    """Authentication endpoint for spectral entities! 👻.

    This endpoint handles user authentication and JWT token generation.
    Successfull authentication returns :
    a token for accessing protected endpoints.
    """

    @log_me(component="api")
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
        """Authenticate and receive a haunted token! 🎭"""
        data = request.get_json()

        try:
            user = facade.login(
                email=data.get("email"), password=data.get("password")
            )

            # Générer le token avec les claims appropriés
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

        except ValueError as e:
            return {"message": str(e)}, 401
