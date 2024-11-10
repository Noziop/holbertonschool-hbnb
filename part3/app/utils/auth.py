"""Authentication decorators for our haunted API! 👻"""

from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_restx import abort


def auth_required(admin_only: bool = False, owner_only: bool = False):
    """Protège nos endpoints avec des pouvoirs mystiques ! 🔮

    Args:
        admin_only (bool): Réservé au Head Ghost 👑
        owner_only (bool): Vérifie si le fantôme est propriétaire 👻
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Vérifie le token JWT
            verify_jwt_in_request()
            claims = get_jwt()

            # Vérifie si le fantôme n'a pas été exorcisé
            if not claims.get("is_active"):
                abort(401, "This ghost has been exorcised! 👻")

            # Vérifie les droits admin si nécessaire
            if admin_only and not claims.get("is_admin"):
                abort(403, "Only the Head Ghost can do that! 👑")

            # Vérifie la propriété si nécessaire
            if owner_only:
                resource_id = kwargs.get("id")  # ou user_id, place_id, etc.
                if not (
                    claims.get("is_admin")
                    or claims.get("user_id") == resource_id
                ):
                    abort(403, "This isn't your haunt! 👻")

            return fn(*args, **kwargs)

        return decorator

    return wrapper


# Alias pratiques
admin_only = auth_required(admin_only=True)
owner_only = auth_required(owner_only=True)
