# app/models/placeamenity.py
"""PlaceAmenity model module: The bridge between haunted places and their features! 👻"""
from typing import TYPE_CHECKING, Any, Dict, Optional

from app.models.basemodel import BaseModel

# Conditional imports for type hints
if TYPE_CHECKING:
    from app.models.amenity import Amenity
    from app.models.place import Place


class PlaceAmenity(BaseModel):
    """PlaceAmenity: A supernatural link between places and amenities! 🔗"""

    def __init__(self, place_id: str, amenity_id: str, **kwargs):
        """Initialize a new haunted connection! ✨"""
        self.logger.debug(
            f"Creating new PlaceAmenity link between place {place_id} and amenity {amenity_id}"
        )
        super().__init__(**kwargs)

        # Check for existing link
        existing = self.get_by_attr(place_id=place_id, amenity_id=amenity_id)
        if existing:
            error_msg = (
                f"Link already exists between place {place_id} and amenity {amenity_id}"
            )
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Required attributes
        self.place_id = self._validate_place_id(place_id)
        self.amenity_id = self._validate_amenity_id(amenity_id)

        self.logger.info(f"Created new PlaceAmenity with ID: {self.id}")

    def _validate_place_id(self, place_id: str) -> str:
        """Validate place ID! 🏰"""
        self.logger.debug(f"Validating place ID: {place_id}")
        try:
            from app.models.place import Place

            if not Place.get_by_id(place_id):
                error_msg = "Invalid place_id"
                self.logger.error(f"Place validation failed: {error_msg}")
                raise ValueError(error_msg)
        except ImportError:
            self.logger.warning("Place model not implemented yet")
        return place_id

    def _validate_amenity_id(self, amenity_id: str) -> str:
        """Validate amenity ID! 🎭"""
        self.logger.debug(f"Validating amenity ID: {amenity_id}")
        try:
            from app.models.amenity import Amenity

            if not Amenity.get_by_id(amenity_id):
                error_msg = "Invalid amenity_id"
                self.logger.error(f"Amenity validation failed: {error_msg}")
                raise ValueError(error_msg)
        except ImportError:
            self.logger.warning("Amenity model not implemented yet")
        return amenity_id

    def to_dict(self) -> Dict[str, Any]:
        """Transform link into dictionary! 📚"""
        self.logger.debug(f"Converting PlaceAmenity {self.id} to dictionary")
        base_dict = super().to_dict()
        link_dict = {"place_id": self.place_id, "amenity_id": self.amenity_id}
        return {**base_dict, **link_dict}
