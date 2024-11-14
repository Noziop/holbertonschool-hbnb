"""Authentication decorators for our haunted API! 👻"""

from functools import wraps

import werkzeug.exceptions
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def auth_required(check_property: bool = False, admin_only: bool = False):
    """Protège nos endpoints avec des pouvoirs mystiques ! 🔮"""

    def actual_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                if not claims.get("is_active"):
                    return {"message": "This ghost has been exorcised! 👻"}, 401

                if not claims.get("user_id"):
                    return {"message": "Authentication required! 👻"}, 401

                if admin_only and not claims.get("is_admin"):
                    return {
                        "message": "Only the Head Ghost can do that! 👑"
                    }, 403

                if check_property:
                    # Si admin, tout est permis
                    if claims.get("is_admin"):
                        return fn(*args, **kwargs)

                    # Pour les places
                    if "place_id" in kwargs:
                        from app.models.place import Place

                        place = Place.get_by_id(kwargs["place_id"])
                        if not place:
                            return {"message": "Place not found! 👻"}, 404
                        if claims.get("user_id") != place.owner_id:
                            return {"message": "This isn't your haunt! 👻"}, 403

                    if "review_id" in kwargs:
                        from app.models.review import Review

                        review = Review.get_by_id(kwargs["review_id"])
                        if not review:
                            return {"message": "Review not found! 👻"}, 404
                        if not (
                            claims.get("is_admin")
                            or claims.get("user_id") == review.user_id
                        ):
                            return {"message": "This isn't your haunt! 👻"}, 403

                    # Pour les utilisateurs
                    elif "user_id" in kwargs:
                        from app.models.user import User

                        user = User.get_by_id(kwargs["user_id"])
                        if not user or not user.is_active:
                            return {
                                "message": "This ghost has been exorcised! 👻"
                            }, 401
                        if claims.get("user_id") != kwargs["user_id"]:
                            return {"message": "This isn't your haunt! 👻"}, 403

                return fn(*args, **kwargs)
            except werkzeug.exceptions.NotFound:
                return {"message": "Resource not found! 👻"}, 404
            except werkzeug.exceptions.Forbidden:
                return {"message": "This isn't your haunt! 👻"}, 403
            except ValueError as e:
                return {"message": str(e)}, 403
            except Exception:
                return {"message": "Authentication required! 👻"}, 401

        return wrapper

    return actual_decorator


# Alias pratiques
user_only = auth_required()  # Authentification simple
admin_only = auth_required(admin_only=True)  # Vérification admin
owner_only = auth_required(check_property=True)  # Vérification propriété
