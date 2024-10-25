"""Module for Amenity class - Where features come back to haunt you! 👻"""
from typing import List, Optional
from datetime import datetime, timezone
import re
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class Amenity(BaseModel):
    """
    Amenity Model: The supernatural features that haunt our places! 🧟‍♀️
    Like ghosts, they appear when you least expect them...
    """
    repository = InMemoryRepository()

    @magic_wand(validate_input(AmenityValidation))
    def __init__(self, name: str, description: str = "", **kwargs):
        """
        Summon a new Amenity from the depths! 🪦
        
        Args:
            name: The cursed name of this feature
            **kwargs: Dark magic attributes
        """
        super().__init__(**kwargs)
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)

    @staticmethod
    @magic_wand()
    def _validate_name(name: str) -> str:
        """
        Validate the dark name of this amenity! 🦇
        
        Raises:
            ValueError: When the spirits reject the name!
        """
        if not name.strip():
            raise ValueError("Empty names anger the spirits! 👻")
        if not re.match(r'^[\w\s-]+$', name):
            msg = "The spirits only accept letters, numbers, spaces, and cursed hyphens! 💀"
            raise ValueError(msg)
        return name.strip()
    
    @staticmethod
    @magic_wand()
    def _validate_description(description: str) -> str:
        """Validate the ghostly description! 👻"""
        if not isinstance(description, str):
            raise ValueError("Description must be a string, like a ghost story! 📖")
        return description.strip() if description else None

    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def create(cls, **kwargs) -> 'Amenity':
        """Create new amenity. Summoning a new feature! 👻"""
        if 'name' not in kwargs:
            raise ValueError("A ghost amenity needs a name! 👻")
        
        if 'name' in kwargs and len(kwargs['name']) < 2:
            raise ValueError("A proper gosthly Amenity name must be at least 2 characters long! 👻")
            
        if cls.get_by_attr(name=kwargs['name']):
            raise ValueError(
                f"Amenity name '{kwargs['name']}' already exists! The spirits are confused! 👻"
            )
        return super().create(**kwargs)

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> 'Amenity':
        """
        Update this cursed feature! 🪦
        
        Raises:
            ValueError: When the dark magic fails!
        """
        if 'name' in data:
            existing = self.get_by_attr(name=data['name'])
            if existing and existing.id != self.id:
                raise ValueError(
                    f"The name '{data['name']}' is already haunting another amenity! 👻"
                )
            self.name = self._validate_name(data['name'])

        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    @classmethod
    @magic_wand()
    def search(cls, **criteria) -> List['Amenity']:
        """Search through the cursed features! Like a supernatural detective! 🔍"""
        if not criteria:
            return cls.get_all()

        results = cls.get_all()
        for attr, value in criteria.items():
            if value is not None:
                results = [
                    amenity for amenity in results
                    if getattr(amenity, attr, None) == value
                ]
        return results

    @magic_wand()
    def get_places(self) -> List['Place']:
        """Find all places haunted by this feature! 🏚️"""
        from .placeamenity import PlaceAmenity
        from .place import Place
        place_amenities = PlaceAmenity.get_by_attr(multiple=True, amenity_id=self.id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """Transform this cursed feature into mortal-readable format! 📜"""
        base_dict = super().to_dict()
        return {**base_dict, 'name': self.name, 'description': self.description}