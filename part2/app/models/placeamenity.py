"""PlaceAmenity Module: The matchmaker of our app! 💘"""
from typing import List, Optional
from datetime import datetime, timezone
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class PlaceAmenity(BaseModel):
    """PlaceAmenity: Future DB-ready, currently serving looks! 💅"""
    repository = InMemoryRepository()

    @magic_wand(validate_input(PlaceAmenityValidation))
    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.amenity_id = self._validate_id(amenity_id, "amenity_id")

    @staticmethod
    @magic_wand()
    def _validate_id(id_value: str, field_name: str) -> str:
        if not isinstance(id_value, str):
            raise ValueError(f"{field_name} must be a string! 💅")
        if not id_value.strip():
            raise ValueError(f"{field_name} cannot be empty!")
        return id_value.strip()

    @classmethod
    @magic_wand(
        validate_input(PlaceAmenityValidation),
        validate_entity(('Place', 'place_id'), ('Amenity', 'amenity_id'))
    )
    def create(cls, place_id: str, amenity_id: str, **kwargs) -> 'PlaceAmenity':
        pa = cls(place_id, amenity_id, **kwargs)
        cls.repository.add(pa)
        return pa

    @classmethod
    @magic_wand(
        validate_input({'place_id': str}), 
        validate_entity('Place', 'place_id')
    )
    def get_by_place(cls, place_id: str) -> List['PlaceAmenity']:
        return cls.repository.get_by_attribute('place_id', place_id, multiple=True)

    @classmethod
    @magic_wand(
        validate_input({'amenity_id': str}), 
        validate_entity('Amenity', 'amenity_id')
    )
    def get_by_amenity(cls, amenity_id: str) -> List['PlaceAmenity']:
        return cls.repository.get_by_attribute('amenity_id', amenity_id, multiple=True)

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> 'PlaceAmenity':
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            elif key in ['place_id', 'amenity_id']:
                setattr(self, key, self._validate_id(value, key))
            else:
                raise ValueError(f"Invalid attribute: {key}")
        
        self.updated_at = datetime.now(timezone.utc)
        return self

    @classmethod
    @magic_wand()
    def delete_by_place_and_amenity(
        cls, 
        place_id: str, 
        amenity_id: str
    ) -> bool:
        matches = cls.repository.get_by_attribute(
            'place_id', 
            place_id, 
            multiple=True
        )
        if matches:
            matches = [m for m in matches if m.amenity_id == amenity_id]
            for m in matches:
                m.delete()
            return True
        return False

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        }