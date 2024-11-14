"""API initialization and configuration! 👻."""

from flask import Blueprint
from flask_restx import Api

from app.utils import admin_only, auth_required, log_me, owner_only, user_only

from .v1.amenities import ns as amenities_ns
from .v1.auth import ns as auth_ns
from .v1.places import ns as places_ns
from .v1.reviews import ns as reviews_ns
from .v1.users import ns as users_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(
    api_bp,
    version="1.0",
    title="🏚️ Haunted - BnB API 🏚️",
    description="A haunted vacation rental API 👻",
)

# Ajout des namespaces à l'API
api.add_namespace(auth_ns, path="/login")
api.add_namespace(users_ns, path="/users")
api.add_namespace(places_ns, path="/places")
api.add_namespace(reviews_ns, path="/reviews")
api.add_namespace(amenities_ns, path="/amenities")

__all__ = [
    "api_bp",
    "api",
    "auth_required",
    "admin_only",
    "owner_only",
    "user_only",
    "log_me",
]
