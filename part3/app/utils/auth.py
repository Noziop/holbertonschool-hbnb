"""Authentication decorators for our haunted API! 👻"""

from functools import wraps

import werkzeug.exceptions
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def auth_required(check_property: bool = False, admin_only: bool = False):
    """Protège nos endpoints avec des pouvoirs mystiques ! 🔮"""

    def actual_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            print("\n=== Debug auth_required decorator ===")
            print(f"check_property: {check_property}")
            print(f"admin_only: {admin_only}")
            print(f"kwargs: {kwargs}")

            try:
                verify_jwt_in_request()
                claims = get_jwt()
                print(f"Claims: {claims}")

                if not claims.get("is_active"):
                    print("User not active -> 401")
                    return {"message": "This ghost has been exorcised! 👻"}, 401

                if not claims.get("user_id"):
                    print("No user_id -> 401")
                    return {"message": "Authentication required! 👻"}, 401

                if admin_only and not claims.get("is_admin"):
                    print("Admin required but user is not admin -> 403")
                    return {
                        "message": "Only the Head Ghost can do that! 👑"
                    }, 403

                if check_property:
                    print("Checking property...")
                    # Si admin, tout est permis
                    if claims.get("is_admin"):
                        print("Admin bypass -> continue")
                        return fn(*args, **kwargs)

                    # Pour les places
                    if "place_id" in kwargs:
                        print(f"Checking place_id: {kwargs['place_id']}")
                        from app.models.place import Place

                        place = Place.get_by_id(kwargs["place_id"])
                        if not place:
                            print("Place not found -> 404")
                            return {"message": "Place not found! 👻"}, 404
                        if claims.get("user_id") != place.owner_id:
                            print("User is not place owner -> 403")
                            return {"message": "This isn't your haunt! 👻"}, 403

                    if "review_id" in kwargs:
                        from app.models.review import Review

                        print(f"Review ID: {kwargs['review_id']}")
                        review = Review.get_by_id(kwargs["review_id"])
                        if not review:
                            print("Review not found!")
                            return {"message": "Review not found! 👻"}, 404
                        if not (
                            claims.get("is_admin")
                            or claims.get("user_id") == review.user_id
                        ):
                            print("Not admin or owner!")
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

                print("All checks passed -> continue to route")
                return fn(*args, **kwargs)
            except werkzeug.exceptions.NotFound as e:
                print(f"NotFound exception -> 404: {str(e)}")
                return {"message": "Resource not found! 👻"}, 404
            except werkzeug.exceptions.Forbidden as e:
                print(f"Forbidden exception -> 403: {str(e)}")
                return {"message": "This isn't your haunt! 👻"}, 403
            except ValueError as e:
                print(f"ValueError -> 403: {str(e)}")
                return {"message": str(e)}, 403
            except Exception as e:
                print(f"Unexpected error -> 401: {str(e)}")
                return {"message": "Authentication required! 👻"}, 401

        return wrapper

    return actual_decorator


# Alias pratiques
user_only = auth_required()  # Authentification simple
admin_only = auth_required(admin_only=True)  # Vérification admin
owner_only = auth_required(check_property=True)  # Vérification propriété
