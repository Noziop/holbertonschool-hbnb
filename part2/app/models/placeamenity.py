"""PlaceAmenity Module: Where Places and Amenities come back from the dead! 🧟‍♀️"""
from typing import List, Optional
from datetime import datetime, timezone
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class PlaceAmenity(BaseModel):
    """
    PlaceAmenity: The haunted matchmaker of our cursed app! 👻
    Where Places and Amenities have their supernatural rendezvous!
    """
    repository = InMemoryRepository()

    @magic_wand(validate_input(PlaceAmenityValidation))
    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        """Summon a new cursed relationship! 🪦"""
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.amenity_id = self._validate_id(amenity_id, "amenity_id")

    @staticmethod
    @magic_wand()
    def _validate_id(id_value: str, field_name: str) -> str:
        """Validate IDs like a supernatural bouncer! 👻"""
        if not isinstance(id_value, str):
            raise ValueError(f"{field_name} must be a string, mortal! 🧟‍♀️")
        if not id_value.strip():
            raise ValueError(f"Empty {field_name}? The spirits are displeased! 👻")
        return id_value.strip()

    @classmethod
    @magic_wand(
        validate_input(PlaceAmenityValidation),
        validate_entity(('Place', 'place_id'), ('Amenity', 'amenity_id'))
    )
    def create(cls, place_id: str, amenity_id: str, **kwargs) -> 'PlaceAmenity':
        """Create a new cursed bond! The spirits demand it! 🪦"""
        pa = cls(place_id, amenity_id, **kwargs)
        cls.repository.add(pa)
        return pa

    @classmethod
    @magic_wand(
        validate_input({'place_id': str}), 
        validate_entity('Place', 'place_id')
    )
    def get_by_place(cls, place_id: str) -> List['PlaceAmenity']:
        """Find all amenities haunting this place! 👻"""
        return cls.get_by_attr(multiple=True, place_id=place_id)

    @classmethod
    @magic_wand(
        validate_input({'amenity_id': str}), 
        validate_entity('Amenity', 'amenity_id')
    )
    def get_by_amenity(cls, amenity_id: str) -> List['PlaceAmenity']:
        """Find all places cursed by this amenity! 🧟‍♀️"""
        return cls.get_by_attr(multiple=True, amenity_id=amenity_id)

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> 'PlaceAmenity':
        """Update the curse! The spirits are restless! 🦇"""
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            elif key in ['place_id', 'amenity_id']:
                setattr(self, key, self._validate_id(value, key))
            else:
                raise ValueError(f"Invalid attribute: {key}. The spirits reject it! 👻")
        
        self.updated_at = datetime.now(timezone.utc)
        return self

    @classmethod
    @magic_wand()
    def delete_by_place_and_amenity(
        cls, 
        place_id: str, 
        amenity_id: str
    ) -> bool:
        """Break the supernatural bond! Time for an exorcism! 🕯️"""
        cursed_bonds = cls.get_by_attr(
            multiple=True,
            place_id=place_id,
            amenity_id=amenity_id
        )
        if cursed_bonds:
            for bond in cursed_bonds:
                bond.delete()
            return True
        return False

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """Transform this cursed bond into mortal-readable format! 📜"""
        return {
            **super().to_dict(),
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        }