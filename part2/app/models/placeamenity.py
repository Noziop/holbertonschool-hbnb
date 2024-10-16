from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class PlaceAmenity(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, place_id, amenity_id, **kwargs):
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.amenity_id = self._validate_id(amenity_id, "amenity_id")

    @staticmethod
    def _validate_id(id_value, field_name):
        if not isinstance(id_value, str) or not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @classmethod
    def create(cls, place_id, amenity_id, **kwargs):
        place_amenity = cls(place_id, amenity_id, **kwargs)
        cls.repository.add(place_amenity)
        return place_amenity

    @classmethod
    def get_by_place(cls, place_id):
        return [pa for pa in cls.get_all() if pa.place_id == place_id]

    @classmethod
    def get_by_amenity(cls, amenity_id):
        return [pa for pa in cls.get_all() if pa.amenity_id == amenity_id]

    @classmethod
    def get_places(cls, amenity_id):
        from .place import Place
        place_amenities = cls.get_by_amenity(amenity_id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    def update(self, data):
        if 'place_id' in data:
            self.place_id = self._validate_id(data['place_id'], "place_id")
        if 'amenity_id' in data:
            self.amenity_id = self._validate_id(data['amenity_id'], "amenity_id")
        super().update(data)

    def to_dict(self):
        place_amenity_dict = super().to_dict()
        place_amenity_dict.update({
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        })
        return place_amenity_dict