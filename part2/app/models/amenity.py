from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
import re
from app.utils import *

class Amenity(BaseModel):
    repository = InMemoryRepository()


    @magic_wand(validate_input(AmenityValidation))
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    @magic_wand()
    def _validate_name(name):
        if not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        return name.strip()

    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def create(cls, **kwargs):
        amenity = cls(**kwargs)
        cls.repository.add(amenity)
        return amenity

    @classmethod
    @magic_wand(validate_input(AmenityValidation))
    def get_by_name(cls, name):
        return [amenity for amenity in cls.get_all() if amenity.name.lower() == name.lower()]

    @classmethod
    @magic_wand(validate_input({'keyword': str}))
    def search(cls, keyword):
        return [amenity for amenity in cls.get_all() if keyword.lower() in amenity.name.lower()]


    @magic_wand(validate_input({'data': dict}), update_timestamp)
    def update(self, data):
        for key, value in data.items():
            if key == 'name':
                self.name = self._validate_name(value)
            elif key not in ['id', 'created_at', 'updated_at']:
                raise ValueError(f"Invalid attribute: {key}")

    
    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict