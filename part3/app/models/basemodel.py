"""Base model module: The dark foundation of our haunted kingdom! 👻."""

from datetime import datetime
from typing import Any, List, Optional, TypeVar, Union

from app import db
from app.models.mixins import SQLAlchemyMixin
from app.persistence.repository import SQLAlchemyRepository
from app.utils import log_me

# Create a generic type for our supernatural entities
T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model, SQLAlchemyMixin):
    """BaseModel: The supernatural ancestor of all our haunted models! 🏰."""

    __abstract__ = True
    repository = None

    def __init__(self, **kwargs):
        """Initialize a new haunted instance! ✨."""
        super().__init__()

        for key, value in kwargs.items():
            if key in ["created_at", "updated_at"]:
                setattr(self, key, datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @classmethod
    def _get_repo(cls):
        """Get or create repository for this model! 🏰"""
        if cls.repository is None:
            cls.repository = SQLAlchemyRepository(cls)
        return cls.repository

    @log_me(component="business")
    def can_be_managed_by(self, user_id: str, is_admin: bool = False) -> bool:
        """Check if a user can manage (modify/delete) this resource! 🔑"""
        print("\n=== Debug can_be_managed_by ===")
        print(f"Resource type: {self.__class__.__name__}")
        print(f"Resource ID: {self.id}")
        print(f"User ID: {user_id}")
        print(f"Is Admin: {is_admin}")

        # Admin peut tout faire !
        if is_admin:
            print("Admin access granted!")
            return True

        # Cas spécial pour User : l'utilisateur peut se modifier lui-même
        if self.__class__.__name__ == "User":
            print("User self-management check")
            print(f"Self ID: {self.id}")
            print(f"Comparison result: {self.id == user_id}")
            return self.id == user_id

        # Cas spécial pour Review : le créateur peut modifier sa review
        if self.__class__.__name__ == "Review":
            print("Review owner check")
            print(f"Review user_id: {self.user_id}")
            print(f"Comparison result: {self.user_id == user_id}")
            return self.user_id == user_id

        # Pour les autres modèles, vérifier owner_id
        owner_id = getattr(self, "owner_id", None)
        print(f"Owner ID: {owner_id}")
        print(f"Comparison result: {owner_id == user_id}")
        return owner_id == user_id

    @log_me(component="business")
    def save(self) -> T:
        """Save this haunted entity to our realm! 💾"""
        try:
            return self._get_repo().save(self)
        except Exception as e:
            raise ValueError(f"Failed to save: {str(e)}")

    @log_me(component="business")
    def update(self, data: dict) -> T:
        """Update this haunted entity! 🌟"""
        try:
            if not isinstance(data, dict):
                raise ValueError("Update data must be a dictionary")

            protected = {"id", "created_at", "is_deleted"}
            if any(attr in data for attr in protected):
                raise ValueError(
                    f"Cannot modify protected attributes: \
                        {protected & data.keys()}"
                )

            for key, value in data.items():
                setattr(self, key, value)

            return self._get_repo().save(self)
        except Exception as e:
            raise ValueError(f"Update failed: {str(e)} 🔮")

    @log_me(component="business")
    def delete(self) -> bool:
        """Soft delete this entity! 👻"""
        try:
            self.is_deleted = True
            return self._get_repo().update(self)
        except Exception as e:
            raise ValueError(f"Soft delete failed: {str(e)} 🔮")

    @log_me(component="business")
    def hard_delete(self) -> bool:
        """Permanently banish this entity! ⚰️"""
        try:
            return self._get_repo().hard_delete(self)
        except Exception as e:
            raise ValueError(f"Hard delete failed: {str(e)} 🔮")

    @classmethod
    @log_me(component="business")
    def find_by(
        cls, multiple: bool = False, **kwargs
    ) -> Union[Optional[T], List[T]]:
        """Find entities by their attributes! 🔮"""
        return cls._get_repo().get_by_attribute(multiple=multiple, **kwargs)

    @classmethod
    @log_me(component="business")
    def get_by_email(cls, email: str) -> Optional[T]:
        """Summon an entity by its email! 📧"""
        return cls._get_repo().get_by_email(email)

    @classmethod
    @log_me(component="business")
    def get_by_id(cls, id: str) -> Optional[T]:
        """Summon an entity by its ID! 🔍"""
        return cls._get_repo().get(id)

    @classmethod
    @log_me(component="business")
    def get_all(cls) -> List[T]:
        """Summon all entities of this type! 👻"""
        return cls._get_repo().get_all()

    @log_me(component="business")
    def to_dict(self) -> dict:
        """Transform this entity into a dictionary! 📚"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if not column.name.startswith("_")
        }
