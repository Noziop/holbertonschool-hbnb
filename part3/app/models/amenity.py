"""Amenity model module: Where features come back to haunt you! 👻."""

import re
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy.orm import relationship

from app import db
from app.models.basemodel import BaseModel
from app.utils import log_me

if TYPE_CHECKING:  # noqa: F401
    from app.models.place import Place  # noqa: F401


class AmenityCategory(str, Enum):
    """The different types of supernatural features! 🎭."""

    SAFETY = "safety"
    COMFORT = "comfort"
    ENTERTAINMENT = "entertainment"
    SUPERNATURAL = "supernatural"
    BLOCKED = "blocked"  # Pour le soft delete


class Amenity(BaseModel):
    """Amenity: A supernatural feature for our haunted places! 🎭."""

    # SQLAlchemy columns
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.Enum(AmenityCategory, values_callable=lambda x: [e.value for e in x]),
        default=AmenityCategory.SUPERNATURAL,
        nullable=False,
    )

    def __init__(
        self,
        name: str,
        description: str,
        category: str = AmenityCategory.SUPERNATURAL.value,
        **kwargs,
    ):
        """Initialize a new supernatural feature! ✨."""
        super().__init__(**kwargs)

        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.category = self._validate_category(category)

    @log_me(component="business")
    def _validate_name(self, name: str) -> str:
        """Validate amenity name! 🏷️."""
        if not name.strip():
            raise ValueError("Name cannot be empty!")

        if not re.match(r"^[\w\s-]+$", name):
            raise ValueError(
                "Name can only contain letters, numbers, spaces, and hyphens!"
            )

        # Vérifier l'unicité du nom avec SQLAlchemy
        existing = self.query.filter_by(name=name.strip()).first()
        if existing and existing.id != self.id:
            raise ValueError(f"Name '{name}' already exists!")

        return name.strip()

    @log_me(component="business")
    def _validate_description(self, description: str) -> str:
        """Validate amenity description! 📝."""
        if not isinstance(description, str):
            raise ValueError("Description must be a string!")
        return description.strip() if description else ""

    @log_me(component="business")
    def _validate_category(self, category: str) -> AmenityCategory:
        """Validate amenity category! 🏷️."""
        try:
            return AmenityCategory(category)
        except ValueError:
            raise ValueError(
                "Category must be one of: "
                f"{', '.join(c.value for c in AmenityCategory)}"
            )

    @log_me(component="business")
    def update(self, data: dict) -> "Amenity":
        """Update amenity attributes! 🔄."""
        try:
            # Validate name if present
            if "name" in data:
                data["name"] = self._validate_name(data["name"])

            # Validate description if present
            if "description" in data:
                data["description"] = self._validate_description(
                    data["description"]
                )

            # Validate category if present
            if "category" in data:
                data["category"] = self._validate_category(data["category"])

            return super().update(data)
        except Exception as error:
            raise ValueError(f"Failed to update Amenity: {str(error)}")

    @log_me(component="business")
    def delete(self) -> bool:
        """Soft delete this supernatural feature! 🌙."""
        try:
            return self.update({"category": AmenityCategory.BLOCKED})
        except Exception as error:
            raise ValueError(f"Failed to soft delete Amenity: {str(error)}")

    @log_me(component="business")
    def hard_delete(self) -> bool:
        """Permanently delete amenity and all related links! ⚰️."""
        try:
            # Avec SQLAlchemy et la relation many-to-many,
            # les liens seront automatiquement supprimés
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            raise ValueError(f"Failed to hard delete Amenity: {str(error)}")

    @log_me(component="business")
    def get_places(self) -> List["Place"]:
        """Get all places with this amenity! 🏰."""
        # Grâce à la relation SQLAlchemy
        # on peut directement accéder aux places
        return [
            place
            for place in self.places
            if not place.is_deleted and place.status != "blocked"
        ]

    @log_me(component="business")
    def to_dict(self) -> Dict[str, Any]:
        """Transform amenity into dictionary! 📚."""
        base_dict = super().to_dict()
        amenity_dict = {
            "name": self.name,
            "description": self.description,
            "category": self.category.value if self.category else None,
            # Optionnellement, inclure les places liées
            "places": [
                place.to_dict()
                for place in self.places
                if not place.is_deleted and place.status != "blocked"
            ],
        }
        return {**base_dict, **amenity_dict}
