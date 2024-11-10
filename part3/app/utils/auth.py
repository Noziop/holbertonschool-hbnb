"""Authentication decorators for our haunted API! 👻"""

from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request


def ouija_only(admin_required: bool = False):
    """Magic Decorator to protect our endpoints ! 🔮

    Args:
        admin_required (bool): if True, only admin users can access the endpoint
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            # Is ghost dead or dead-dead?
            if not claims.get("is_active"):
                return {"message": "This ghost has been exorcised! 👻"}, 401

            # is this ghost the Head Ghost?
            if admin_required and not claims.get("is_admin"):
                return {"message": "Only the Head Ghost can do that! 👑"}, 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
