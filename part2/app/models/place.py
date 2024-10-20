from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
from app.utils import *
import math

class Place(BaseModel):
    repository = InMemoryRepository()

    @magic_wand(validate_input(PlaceValidation), validate_entity('User', 'owner_id'))
    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, 
                 price_by_night, latitude, longitude, owner_id, city="", country="", **kwargs):
        from .user import User
        super().__init__(**kwargs)
        self.name = self._validate_string(name, "name")
        self.description = self._validate_string(description, "description")
        self.number_rooms = self._validate_positive_integer(number_rooms, "number_rooms")
        self.number_bathrooms = self._validate_positive_integer(number_bathrooms, "number_bathrooms")
        self.max_guest = self._validate_positive_integer(max_guest, "max_guest")
        self.price_by_night = self._validate_positive_float(price_by_night, "price_by_night")
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.city = self._validate_string(city, "city")
        self.country = self._validate_string(country, "country")
        self.owner_id = self._validate_string(owner_id, "owner_id")
        self.amenity_ids = []
        self.review_ids = []

    @staticmethod
    @magic_wand()
    def _validate_string(value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        return value.strip()

    @staticmethod
    @magic_wand()
    def _validate_positive_integer(value, field_name):
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive integer")
        return value

    @staticmethod
    @magic_wand()
    def _validate_positive_float(value, field_name):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive number")
        return value

    @staticmethod
    @magic_wand()
    def _validate_latitude(value):
        try:
            value = float(value)
            if not -90 <= value <= 90:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number between -90 and 90")
        return value

    @staticmethod
    @magic_wand()
    def _validate_longitude(value):
        try:
            value = float(value)
            if not -180 <= value <= 180:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number between -180 and 180")
        return value

    @classmethod
    @magic_wand()
    def create(cls, **kwargs):
        try:
            place = cls(**kwargs)
            cls.repository.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Failed to create place: {str(e)}")

    @classmethod
    @magic_wand()
    def get_by_city(cls, city):
        return [place for place in cls.get_all() if place.city.lower() == city.lower()]

    @classmethod
    @magic_wand()
    def get_by_country(cls, country):
        return [place for place in cls.get_all() if place.country.lower() == country.lower()]

    @classmethod
    @magic_wand()
    def get_by_price_range(cls, min_price, max_price):
        return [place for place in cls.get_all() if min_price <= place.price_by_night <= max_price]

    @classmethod
    @magic_wand()
    def get_by_capacity(cls, min_guests):
        return [place for place in cls.get_all() if place.max_guest >= min_guests]

    @classmethod
    @magic_wand()
    def get_by_location(cls, latitude, longitude, radius):
        def distance(lat1, lon1, lat2, lon2):
            R = 6371  # Rayon de la Terre en km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        return [place for place in cls.get_all() 
                if distance(latitude, longitude, place.latitude, place.longitude) <= radius]

    @classmethod
    @magic_wand()
    def search(cls, keywords):
        keywords = keywords.lower()
        return [place for place in cls.get_all() 
                if keywords in place.name.lower() 
                or keywords in place.description.lower() 
                or keywords in place.city.lower() 
                or keywords in place.country.lower()]
    

    @magic_wand(validate_input(PlaceValidation), validate_entity('User', 'owner_id'))
    def update(self, data):
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary")
        
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue  # Skip these fields
            elif hasattr(self, f'_validate_{key}'):
                # Call the specific validation method for this attribute
                validated_value = getattr(self, f'_validate_{key}')(value)
                setattr(self, key, validated_value)
            elif key in ['number_rooms', 'number_bathrooms', 'max_guest']:
                # Use the _validate_positive_integer method for these fields
                setattr(self, key, self._validate_positive_integer(value, key))
            elif key == 'price_by_night':
                # Use the _validate_positive_float method for price_by_night
                setattr(self, key, self._validate_positive_float(value, key))
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        
        self.updated_at = datetime.now(timezone.utc)


    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def get_amenities(self):
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        place_amenities = PlaceAmenity.get_by_place(self.id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]


    @magic_wand(validate_entity('Amenity', 'amenity_id'), update_timestamp)
    def add_amenity(self, amenity):
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.create(place_id=self.id, amenity_id=amenity.id)


    @magic_wand(validate_entity('Amenity', 'amenity_id'), update_timestamp)
    def remove_amenity(self, amenity):
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.delete_by_place_and_amenity(self.id, amenity.id)


    @magic_wand(validate_entity('Review', 'review_id'), update_timestamp)
    def get_reviews(self):
        from .review import Review
        return Review.get_by_place(self.id)

    # Nous n'avons pas besoin de méthodes add_review ou remove_review ici,
    # car ces opérations seront gérées directement dans le modèle Review.

    @magic_wand()
    @to_dict(exclude=[])
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