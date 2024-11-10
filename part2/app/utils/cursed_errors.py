# app/utils/cursed_errors.py
"""Custom exceptions for our haunted app! 👻"""


class HauntedException(Exception):
    """Base exception for all our haunted errors! 🎭"""

    def __init__(self, message: str = "A spooky error occurred!"):
        self.message = message
        super().__init__(self.message)


class ValidationError(HauntedException):
    """Raised when a ghost fails validation! 👻"""

    def __init__(self, message: str = "Validation failed!"):
        super().__init__(f"👻 Boo! {message}")


class NotFoundError(HauntedException):
    """Raised when a spirit cannot be found! 🔍"""

    def __init__(self, entity: str, identifier: str):
        super().__init__(f"🔍 The {entity} with id '{identifier}' has vanished!")


class UniqueConstraintError(HauntedException):
    """Raised when a unique constraint is violated! ⚡"""

    def __init__(self, field: str, value: str):
        super().__init__(f"⚡ Another ghost already haunts this {field}: '{value}'")


class RelationshipError(HauntedException):
    """Raised when a relationship constraint is violated! 🔗"""

    def __init__(self, message: str):
        super().__init__(f"🔗 {message}")


class DatabaseError(HauntedException):
    """Raised when the haunted database misbehaves! 💀"""

    def __init__(self, operation: str, details: str = None):
        message = f"💀 Database operation '{operation}' failed!"
        if details:
            message += f" Details: {details}"
        super().__init__(message)
