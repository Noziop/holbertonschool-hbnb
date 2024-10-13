from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class Place(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, 
                 price_by_night, latitude, longitude, owner_id, city="", country=""):
        super().__init__()
        self.name = name
        self.description = description
        self.number_rooms = self._validate_positive_integer(number_rooms, "number_rooms")
        self.number_bathrooms = self._validate_positive_integer(number_bathrooms, "number_bathrooms")
        self.max_guest = self._validate_positive_integer(max_guest, "max_guest")
        self.price_by_night = self._validate_positive_float(price_by_night, "price_by_night")
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.city = city
        self.country = country
        self.owner_id = owner_id
        self.amenity_ids = []
        self.review_ids = []

    @staticmethod
    def _validate_positive_integer(value, field_name):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be a positive integer")
        return value

    @staticmethod
    def _validate_positive_float(value, field_name):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{field_name} must be a positive number")
        return float(value)

    @staticmethod
    def _validate_latitude(value):
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @staticmethod
    def _validate_longitude(value):
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    @classmethod
    def create(cls, **kwargs):
        place = cls(**kwargs)
        cls.repository.add(place)
        return place

    @classmethod
    def get_by_id(cls, place_id):
        return cls.repository.get(place_id)

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.repository.update(self.id, self)

    def delete(self):
        self.repository.delete(self.id)

    def add_amenity_id(self, amenity_id):
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)

    def remove_amenity_id(self, amenity_id):
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)

    def add_review_id(self, review_id):
        if review_id not in self.review_ids:
            self.review_ids.append(review_id)

    def remove_review_id(self, review_id):
        if review_id in self.review_ids:
            self.review_ids.remove(review_id)

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict.update({
            'name': self.name,
            'description': self.description,
            'number_rooms': self.number_rooms,
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'price_by_night': self.price_by_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'city': self.city,
            'country': self.country,
            'amenity_ids': self.amenity_ids,
            'review_ids': self.review_ids
        })
        return place_dict