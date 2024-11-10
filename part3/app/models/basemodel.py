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
    repository = SQLAlchemyRepository()

    def __init__(self, **kwargs):
        """Initialize a new haunted instance! ✨."""
        super().__init__()  # Important pour SQLAlchemy

        # Handle datetime conversions and other attributes
        for key, value in kwargs.items():
            if key in ["created_at", "updated_at"]:
                setattr(self, key, datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @log_me(component="business")
    def save(self) -> T:
        """Save instance to repository! 📜."""
        try:
            self.repository.add(self)
            return self
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Save operation failed: {str(e)} 🔮")

    @log_me(component="business")
    def update(self, data: dict) -> T:
        """Update instance attributes! ✨."""
        try:
            # Garde tes validations actuelles
            if not isinstance(data, dict):
                raise ValueError("Update data must be a dictionary")

            protected = {"id", "created_at", "is_deleted"}
            if any(attr in data for attr in protected):
                raise ValueError(
                    f"Cannot modify protected \
                    attributes: {protected & data.keys()}"
                )

            # Update attributes
            for key, value in data.items():
                setattr(self, key, value)

            # SQLAlchemy mettra à jour updated_at automatiquement
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Update operation failed: {str(e)}")

    @log_me(component="business")
    def hard_delete(self) -> bool:
        """Permanently delete instance from repository! ⚰️."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Delete operation failed: {str(e)}")

    @log_me(component="business")
    @classmethod
    def get_all_by_type(cls) -> List[T]:
        """Get all instances of specific type! 👻."""
        return cls.query.filter_by(is_deleted=False).all()

    @log_me(component="business")
    @classmethod
    def get_by_id(cls: type[T], id: str) -> T:
        """Retrieve instance by ID! 👻."""
        obj = cls.query.get(id)
        if obj is None:
            raise ValueError(f"Entity not found: {id}")
        return obj

    @log_me(component="business")
    @classmethod
    def get_by_attr(
        cls: type[T], multiple: bool = False, **kwargs: Any
    ) -> Union[Optional[T], List[T]]:
        """Search instances by attributes! 🔮."""
        query = cls.query.filter_by(**kwargs, is_deleted=False)
        return query.all() if multiple else query.first()

    @log_me(component="business")
    def to_dict(self) -> dict:
        """Convert instance to dictionary! 📚."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if not column.name.startswith("_")
        }
