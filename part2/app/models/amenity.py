from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
import re

class Amenity(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        return name.strip()

    @classmethod
    def create(cls, **kwargs):
        try:
            amenity = cls(**kwargs)
            cls.repository.add(amenity)
            return amenity
        except ValueError as e:
            raise ValueError(f"Failed to create amenity: {str(e)}")

    @classmethod
    def get_by_name(cls, name):
        return [amenity for amenity in cls.get_all() if amenity.name.lower() == name.lower()]

    @classmethod
    def search(cls, keyword):
        return [amenity for amenity in cls.get_all() if keyword.lower() in amenity.name.lower()]

    @classmethod
    def get_places(cls, amenity_id):
        from .placeamenity import PlaceAmenity
        from .place import Place
        place_amenities = PlaceAmenity.get_by_amenity(amenity_id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    def update(self, data):
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary")
        
        for key, value in data.items():
            if key == 'name':
                self.name = self._validate_name(value)
            elif key not in ['id', 'created_at', 'updated_at']:
                raise ValueError(f"Invalid attribute: {key}")
        
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
