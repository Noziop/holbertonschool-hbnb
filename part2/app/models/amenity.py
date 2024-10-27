# app/models/amenity.py
"""Amenity model module: Where features come back to haunt you! 👻"""
from typing import Optional, Dict, Any, List, TYPE_CHECKING
import re
from app.models.basemodel import BaseModel

# Conditional imports for type hints
if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.placeamenity import PlaceAmenity

class Amenity(BaseModel):
    """Amenity: A supernatural feature in our haunted realm! 🧟‍♀️"""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        **kwargs
    ):
        """Initialize a new haunted amenity! ✨"""
        self.logger.debug(f"Creating new Amenity with name: {name}")
        super().__init__(**kwargs)
        
        # Required attributes
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        
        self.logger.info(f"Created new Amenity with ID: {self.id}")

    def _validate_name(self, name: str) -> str:
        """Validate amenity name! 🏷️"""
        self.logger.debug(f"Validating amenity name: {name}")
        if not name.strip():
            error_msg = "Name cannot be empty!"
            self.logger.error(f"Name validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.match(r'^[\w\s-]+$', name):
            error_msg = "Name can only contain letters, numbers, spaces, and hyphens!"
            self.logger.error(f"Name validation failed: {error_msg}")
            raise ValueError(error_msg)
        return name.strip()

    def _validate_description(self, description: str) -> str:
        """Validate amenity description! 📝"""
        self.logger.debug("Validating amenity description")
        if not isinstance(description, str):
            error_msg = "Description must be a string!"
            self.logger.error(f"Description validation failed: {error_msg}")
            raise ValueError(error_msg)
        return description.strip() if description else ""

    def update(self, data: dict) -> 'Amenity':
        """Update amenity attributes! 🔄"""
        self.logger.debug(f"Attempting to update Amenity: {self.id}")
        try:
            # Validate name if present
            if 'name' in data:
                existing = self.get_by_attr(name=data['name'])
                if existing and existing.id != self.id:
                    error_msg = f"Name '{data['name']}' already exists!"
                    self.logger.error(f"Update failed: {error_msg}")
                    raise ValueError(error_msg)
                data['name'] = self._validate_name(data['name'])
            
            # Validate description if present
            if 'description' in data:
                data['description'] = self._validate_description(data['description'])
            
            return super().update(data)
        except Exception as e:
            self.logger.error(f"Failed to update Amenity: {str(e)}")
            raise

    def get_places(self) -> List['Place']:
        """Get all places with this amenity! 🏰"""
        self.logger.debug(f"Getting places for Amenity: {self.id}")
        try:
            from app.models.place import Place
            from app.models.placeamenity import PlaceAmenity
            
            place_amenities = PlaceAmenity.get_by_attr(multiple=True, amenity_id=self.id)
            return [Place.get_by_id(pa.place_id) for pa in place_amenities]
        except ImportError:
            self.logger.warning("Place/PlaceAmenity models not implemented yet")
            return []

    def to_dict(self) -> Dict[str, Any]:
        """Transform amenity into dictionary! 📚"""
        self.logger.debug(f"Converting amenity {self.id} to dictionary")
        base_dict = super().to_dict()
        amenity_dict = {
            'name': self.name,
            'description': self.description
        }
        return {**base_dict, **amenity_dict}