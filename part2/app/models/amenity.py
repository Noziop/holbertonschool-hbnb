from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
import re

class Amenity(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        return name.strip()

    @classmethod
    def create(cls, name):
        amenity = cls(name)
        cls.repository.add(amenity)
        return amenity

    @classmethod
    def get_by_id(cls, amenity_id):
        return cls.repository.get(amenity_id)

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    def update(self, data):
        if 'name' in data:
            self.name = self._validate_name(data['name'])
        self.repository.update(self.id, self)

    def delete(self):
        self.repository.delete(self.id)

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict