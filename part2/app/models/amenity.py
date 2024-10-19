from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
import re
from app.utils.magic_wands import log_action, error_handler, validate_input, update_timestamp, to_dict_decorator

class Amenity(BaseModel):
    repository = InMemoryRepository()

    @log_action
    @error_handler
    @validate_input(name=str)
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = self._validate_name(name)

    @staticmethod
    @log_action
    @error_handler
    def _validate_name(name):
        if not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not re.match(r'^[\w\s-]+$', name):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        return name.strip()

    @classmethod
    @log_action
    @error_handler
    @validate_input(name=str)
    def create(cls, **kwargs):
        amenity = cls(**kwargs)
        cls.repository.add(amenity)
        return amenity

    @classmethod
    @log_action
    @error_handler
    @validate_input(name=str)
    def get_by_name(cls, name):
        return [amenity for amenity in cls.get_all() if amenity.name.lower() == name.lower()]

    @classmethod
    @log_action
    @error_handler
    @validate_input(keyword=str)
    def search(cls, keyword):
        return [amenity for amenity in cls.get_all() if keyword.lower() in amenity.name.lower()]

    @log_action
    @error_handler
    @update_timestamp
    @validate_input(data=dict)
    def update(self, data):
        for key, value in data.items():
            if key == 'name':
                self.name = self._validate_name(value)
            elif key not in ['id', 'created_at', 'updated_at']:
                raise ValueError(f"Invalid attribute: {key}")

    @to_dict_decorator()
    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict