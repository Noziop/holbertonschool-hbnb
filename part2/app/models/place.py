from .basemodel import BaseModel
from datetime import datetime, timezone
from .review import Review
import math
from app.persistence.repository import InMemoryRepository
from .review import Review

class Place(BaseModel):
    repository = InMemoryRepository()

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
    def _validate_string(value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        return value.strip()

    @staticmethod
    def _validate_positive_integer(value, field_name):
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive integer")
        return value

    @staticmethod
    def _validate_positive_float(value, field_name):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive number")
        return value

    @staticmethod
    def _validate_latitude(value):
        try:
            value = float(value)
            if not -90 <= value <= 90:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number between -90 and 90")
        return value

    @staticmethod
    def _validate_longitude(value):
        try:
            value = float(value)
            if not -180 <= value <= 180:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number between -180 and 180")
        return value

    @classmethod
    def create(cls, name, description, number_rooms, number_bathrooms, max_guest, 
            price_by_night, latitude, longitude, owner_id, city="", country="", **kwargs):
        try:
            place = cls(name, description, number_rooms, number_bathrooms, max_guest, 
                        price_by_night, latitude, longitude, owner_id, city, country, **kwargs)
            cls.repository.add(place)
            return place
        except Exception as e:
            raise ValueError(f"Failed to create place: {str(e)}")

    @classmethod
    def get_by_id(cls, place_id):
        place = cls.repository.get(place_id)
        if place is None:
            raise ValueError(f"No place found with id: {place_id}")
        return place

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    @classmethod
    def get_by_city(cls, city):
        return [place for place in cls.get_all() if place.city.lower() == city.lower()]

    @classmethod
    def get_by_country(cls, country):
        return [place for place in cls.get_all() if place.country.lower() == country.lower()]

    @classmethod
    def get_by_max_guest(cls, max_guest):
        return [place for place in cls.get_all() if place.max_guest >= max_guest]

    @classmethod
    def get_by_price_range(cls, min_price, max_price):
        return [place for place in cls.get_all() if min_price <= place.price_by_night <= max_price]

    @classmethod
    def get_by_amenity(cls, amenity_id):
        return [place for place in cls.get_all() if amenity_id in place.amenity_ids]

    @classmethod
    def get_by_rating(cls, min_rating):
        all_places = cls.get_all()
        rated_places = []
        lower_rated_places = []
        for place in all_places:
            reviews = Review.get_by_place(place.id)
            if reviews:
                average_rating = sum(review.rating for review in reviews) / len(reviews)
                if average_rating >= min_rating:
                    rated_places.append((place, average_rating))
                elif average_rating >= min_rating - 1:  # Pour les suggestions
                    lower_rated_places.append((place, average_rating))
        
        rated_places.sort(key=lambda x: x[1], reverse=True)
        lower_rated_places.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'matching': [place for place, _ in rated_places],
            'suggestions': [place for place, _ in lower_rated_places]
        }
    
    @classmethod
    def get_by_price_range(cls, min_price, max_price):
        return [place for place in cls.get_all() if min_price <= place.price_by_night <= max_price]
    
    @classmethod
    def get_by_capacity(cls, min_guests):
        return [place for place in cls.get_all() if place.max_guest >= min_guests]
    
    @classmethod
    def get_by_location(cls, latitude, longitude, radius):
        def distance(lat1, lon1, lat2, lon2):
            R = 6371  # Rayon de la Terre en km
            dLat = math.radians(float(lat2) - float(lat1))
            dLon = math.radians(float(lon2) - float(lon1))
            a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(float(lat1))) \
                * math.cos(math.radians(float(lat2))) * math.sin(dLon/2) * math.sin(dLon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        all_places = cls.get_all()
        return [place for place in all_places 
                if distance(latitude, longitude, place.latitude, place.longitude) <= radius]

    def calculate_average_rating(self):
        reviews = Review.get_by_place(self.id)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @classmethod
    def get_top_rated(cls, limit=10):
        places = cls.get_all()
        places.sort(key=lambda x: x.calculate_average_rating(), reverse=True)
        return places[:limit]
    
    @classmethod
    def search(cls, keywords):
        keywords = keywords.lower()
        return [place for place in cls.get_all() 
                if keywords in place.name.lower() 
                or keywords in place.description.lower() 
                or keywords in place.city.lower() 
                or keywords in place.country.lower()]

    def update(self, data):
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary")
        
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue  # Skip these fields
            elif hasattr(self, f'_validate_{key}'):
                try:
                    validated_value = getattr(self, f'_validate_{key}')(value)
                    setattr(self, key, validated_value)
                except ValueError as e:
                    raise ValueError(f"Invalid value for {key}: {str(e)}")
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        
        self.updated_at = datetime.now(timezone.utc)
        # We don't call self.repository.update here to avoid the infinite loop


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