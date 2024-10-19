from app.models.basemodel import BaseModel
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.utils.magic_wands import log_action, error_handler, validate_input, update_timestamp, to_dict_decorator, validate_entity_exists

class PlaceAmenity(BaseModel):
    repository = InMemoryRepository()

    @log_action
    @error_handler
    @validate_input(place_id=str, amenity_id=str)
    def __init__(self, place_id, amenity_id, **kwargs):
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.amenity_id = self._validate_id(amenity_id, "amenity_id")

    @staticmethod
    @log_action
    @error_handler
    def _validate_id(id_value, field_name):
        if not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @classmethod
    @log_action
    @error_handler
    @validate_input(place_id=str, amenity_id=str)
    def create(cls, place_id, amenity_id, **kwargs):
        place_amenity = cls(place_id, amenity_id, **kwargs)
        cls.repository.add(place_amenity)
        return place_amenity

    @classmethod
    @log_action
    @error_handler
    @validate_input(place_id=str)
    @validate_entity_exists(lambda place_id: Place.get_by_id(place_id))
    def get_by_place(cls, place_id):
        return [pa for pa in cls.get_all() if pa.place_id == place_id]

    @classmethod
    @log_action
    @error_handler
    @validate_input(amenity_id=str)
    @validate_entity_exists(lambda amenity_id: Amenity.get_by_id(amenity_id))
    def get_by_amenity(cls, amenity_id):
        return [pa for pa in cls.get_all() if pa.amenity_id == amenity_id]

    @classmethod
    @log_action
    @error_handler
    @validate_input(amenity_id=str)
    @validate_entity_exists(lambda amenity_id: Amenity.get_by_id(amenity_id))
    def get_places(cls, amenity_id):
        place_amenities = cls.get_by_amenity(amenity_id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    @log_action
    @error_handler
    @update_timestamp
    @validate_input(data=dict)
    def update(self, data):
        if 'place_id' in data:
            self.place_id = self._validate_id(data['place_id'], "place_id")
        if 'amenity_id' in data:
            self.amenity_id = self._validate_id(data['amenity_id'], "amenity_id")
        super().update(data)

    @to_dict_decorator()
    def to_dict(self):
        place_amenity_dict = super().to_dict()
        place_amenity_dict.update({
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        })
        return place_amenity_dict