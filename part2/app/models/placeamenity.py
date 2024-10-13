from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class PlaceAmenity(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, place_id, amenity_id):
        super().__init__()
        self.place_id = self._validate_id(place_id, "place_id")
        self.amenity_id = self._validate_id(amenity_id, "amenity_id")

    @staticmethod
    def _validate_id(id_value, field_name):
        if not isinstance(id_value, str) or not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @classmethod
    def create(cls, place_id, amenity_id):
        place_amenity = cls(place_id, amenity_id)
        cls.repository.add(place_amenity)
        return place_amenity

    @classmethod
    def get_by_id(cls, place_amenity_id):
        return cls.repository.get(place_amenity_id)

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    @classmethod
    def get_by_place(cls, place_id):
        return [pa for pa in cls.get_all() if pa.place_id == place_id]

    @classmethod
    def get_by_amenity(cls, amenity_id):
        return [pa for pa in cls.get_all() if pa.amenity_id == amenity_id]

    def update(self, data):
        if 'place_id' in data:
            self.place_id = self._validate_id(data['place_id'], "place_id")
        if 'amenity_id' in data:
            self.amenity_id = self._validate_id(data['amenity_id'], "amenity_id")
        self.repository.update(self.id, self)

    def delete(self):
        self.repository.delete(self.id)

    def to_dict(self):
        place_amenity_dict = super().to_dict()
        place_amenity_dict.update({
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        })
        return place_amenity_dict