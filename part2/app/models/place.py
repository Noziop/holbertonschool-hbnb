from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
from app.utils.magic_wands import log_action, validate_input, error_handler, update_timestamp, to_dict_decorator, validate_entity_exists
import math

class Place(BaseModel):
    repository = InMemoryRepository()

    @log_action
    @validate_input(
        name=str,
        description=str,
        number_rooms=int,
        number_bathrooms=int,
        max_guest=int,
        price_by_night=float,
        latitude=float,
        longitude=float,
        owner_id=str,
        city=(str, type(None)),
        country=(str, type(None))
    )
    @error_handler
    @log_action
    @error_handler
    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, 
                 price_by_night, latitude, longitude, owner_id, city="", country="", **kwargs):
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
    @log_action
    @error_handler
    def _validate_string(value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        return value.strip()

    @staticmethod
    @log_action
    @error_handler
    def _validate_positive_integer(value, field_name):
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive integer")
        return value

    @staticmethod
    @log_action
    @error_handler
    def _validate_positive_float(value, field_name):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive number")
        return value

    @staticmethod
    @log_action
    @error_handler
    def _validate_latitude(value):
        try:
            value = float(value)
            if not -90 <= value <= 90:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number between -90 and 90")
        return value

    @staticmethod
    @log_action
    @error_handler
    def _validate_longitude(value):
        try:
            value = float(value)
            if not -180 <= value <= 180:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number between -180 and 180")
        return value

    @classmethod
    @log_action
    @error_handler
    def create(cls, **kwargs):
        try:
            place = cls(**kwargs)
            cls.repository.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Failed to create place: {str(e)}")

    @classmethod
    @log_action
    @error_handler
    def get_by_city(cls, city):
        return [place for place in cls.get_all() if place.city.lower() == city.lower()]

    @classmethod
    @log_action
    @error_handler
    def get_by_country(cls, country):
        return [place for place in cls.get_all() if place.country.lower() == country.lower()]

    @classmethod
    @log_action
    @error_handler
    def get_by_price_range(cls, min_price, max_price):
        return [place for place in cls.get_all() if min_price <= place.price_by_night <= max_price]

    @classmethod
    @log_action
    @error_handler
    def get_by_capacity(cls, min_guests):
        return [place for place in cls.get_all() if place.max_guest >= min_guests]

    @classmethod
    @log_action
    @error_handler
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
    @log_action
    @error_handler
    def search(cls, keywords):
        keywords = keywords.lower()
        return [place for place in cls.get_all() 
                if keywords in place.name.lower() 
                or keywords in place.description.lower() 
                or keywords in place.city.lower() 
                or keywords in place.country.lower()]
    
    @log_action
    @validate_input(data=dict)
    @error_handler
    @update_timestamp
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

    @log_action
    @error_handler
    @validate_entity_exists(lambda self, *args, **kwargs: 
        __import__('app.models.placeamenity').models.placeamenity.PlaceAmenity.get_by_place(self.id))
    def get_amenities(self):
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        place_amenities = PlaceAmenity.get_by_place(self.id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]

    @log_action
    @error_handler
    @update_timestamp
    @validate_entity_exists(lambda self, amenity, *args, **kwargs: 
        __import__('app.models.amenity').models.amenity.Amenity.get_by_id(amenity.id))
    def add_amenity(self, amenity):
        from .placeamenity import PlaceAmenity
        PlaceAmenity.create(place_id=self.id, amenity_id=amenity.id)

    @log_action
    @error_handler
    @update_timestamp
    @validate_entity_exists(lambda self, amenity, *args, **kwargs: 
        __import__('app.models.amenity').models.amenity.Amenity.get_by_id(amenity.id))
    def remove_amenity(self, amenity):
        from .placeamenity import PlaceAmenity
        PlaceAmenity.delete_by_place_and_amenity(self.id, amenity.id)

    @log_action
    @error_handler
    @validate_entity_exists(lambda self, *args, **kwargs: 
        __import__('app.models.review').models.review.Review.get_by_place(self.id))
    def get_reviews(self):
        from .review import Review
        return Review.get_by_place(self.id)

    # Nous n'avons pas besoin de méthodes add_review ou remove_review ici,
    # car ces opérations seront gérées directement dans le modèle Review.

    @to_dict_decorator(exclude=[]) 
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