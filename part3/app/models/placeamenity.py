"""PlaceAmenity : The bridge between haunted places and their features! 👻."""

from typing import Any, Dict

from sqlalchemy.orm import relationship

from app import db
from app.models.basemodel import BaseModel
from app.utils import log_me


class PlaceAmenity(BaseModel):
    """PlaceAmenity: A supernatural link between places and amenities! 🔗."""

    # SQLAlchemy columns
    place_id = db.Column(
        db.String(36), db.ForeignKey("place.id"), nullable=False
    )
    amenity_id = db.Column(
        db.String(36), db.ForeignKey("amenity.id"), nullable=False
    )

    # Relations directes
    place = relationship("Place", back_populates="place_amenities")
    amenity = relationship("Amenity", back_populates="place_amenities")

    # Unique constraint pour éviter les doublons
    __table_args__ = (
        db.UniqueConstraint(
            "place_id", "amenity_id", name="unique_place_amenity"
        ),
    )

    def __init__(self, place_id: str, amenity_id: str, **kwargs):
        """Initialize a new haunted connection! ✨."""
        super().__init__(**kwargs)

        # Required attributes
        self.place_id = self._validate_place_id(place_id)
        self.amenity_id = self._validate_amenity_id(amenity_id)

    @log_me(component="business")
    def _validate_place_id(self, place_id: str) -> str:
        """Validate place ID! 🏰."""
        if not place_id or not isinstance(place_id, str):
            raise ValueError("Place ID must be a non-empty string!")

        from app.models.place import Place

        if not Place.query.get(place_id):
            raise ValueError("Invalid place_id: Place does not exist!")

        return place_id

    @log_me(component="business")
    def _validate_amenity_id(self, amenity_id: str) -> str:
        """Validate amenity ID! 🎭."""
        if not amenity_id or not isinstance(amenity_id, str):
            raise ValueError("Amenity ID must be a non-empty string!")

        from app.models.amenity import Amenity

        if not Amenity.query.get(amenity_id):
            raise ValueError("Invalid amenity_id: Amenity does not exist!")

        return amenity_id

    @log_me(component="business")
    def to_dict(self) -> Dict[str, Any]:
        """Transform link into dictionary! 📚."""
        base_dict = super().to_dict()
        link_dict = {"place_id": self.place_id, "amenity_id": self.amenity_id}
        return {**base_dict, **link_dict}
