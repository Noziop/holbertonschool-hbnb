"""Module for Amenity class."""
from typing import List, Optional
from datetime import datetime, timezone
import re
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class Amenity(BaseModel):
    """
    Amenity Model representing facilities or features available in places.

    Attributes:
        repository (InMemoryRepository):
            Repository for storing Amenity instances
        name (str): Name of the amenity
    """
    repository = InMemoryRepository()

    @magic_wand(validate_input(AmenityValidation))
    def __init__(self, name: str, **kwargs):
        """
        Initialize a new Amenity.

        Args:
            name (str): Name of the amenity
            **kwargs: Additional attributes
        """
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    @magic_wand()
    def _validate_name(name: str) -> str:
        """
        Validate amenity name.

        Args:
            name (str): Name to validate

        Returns:
            str: Validated name

        Raises:
            ValueError: If name is invalid
        """
        if not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            msg = "Name can only contain letters, numbers, spaces, and hyphens"
            raise ValueError(msg)
        return name.strip()

    # Dans Amenity
    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def create(cls, **kwargs) -> 'Amenity':
        """Create new amenity. Summoning a new feature! 👻"""
        if cls.get_by_attr(name=kwargs['name']):
            raise ValueError(
                f"Amenity name '{kwargs['name']}' already exists! The spirits are confused! 👻"
            )
        return super().create(**kwargs)

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> 'Amenity':
        """
        Update Amenity instance.

        Args:
            data (dict): Updated attributes

        Returns:
            Amenity: Updated instance

        Raises:
            ValueError: If update fails or name already exists
        """
        if 'name' in data:
            existing = self.get_by_attr('name', data['name'])
            if existing and existing.id != self.id:
                raise ValueError(
                    f"Amenity with name '{data['name']}' already exists"
                )
            self.name = self._validate_name(data['name'])

        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    @classmethod
    @magic_wand()
    def search(cls, **criteria) -> List['Amenity']:
        """
        Search amenities based on criteria.

        Args:
            **criteria: Search criteria

        Returns:
            List[Amenity]: Matching amenities
        """
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
        """
        Get all places with this amenity.

        Returns:
            List[Place]: Places having this amenity
        """
        from .placeamenity import PlaceAmenity
        from .place import Place
        place_amenities = PlaceAmenity.get_by_amenity(self.id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """
        Convert Amenity to dictionary.

        Returns:
            dict: Amenity attributes
        """
        base_dict = super().to_dict()
        return {**base_dict, 'name': self.name}
