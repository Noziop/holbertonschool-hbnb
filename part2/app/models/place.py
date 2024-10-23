'''Module for Place class.'''
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
from typing import List
from app.utils import *
import math


class Place(BaseModel):
    '''Place Model
        This module defines the Place class, which represents a place or
        property in the application. The Place class inherits from BaseModel
        and includes various attributes and methods for managing place data,
        including validation, filtering, and CRUD operations.

    Attributes:
        repository (InMemoryRepository):
            Repository for storing Place instances.
        name (str): Name of the place.
        description (str): Description of the place.
        number_rooms (int): Number of rooms in the place.
        number_bathrooms (int): Number of bathrooms in the place.
        max_guest (int): Maximum number of guests the place can accommodate.
        price_by_night (float): Price per night for the place.
        latitude (float): Latitude coordinate of the place.
        longitude (float): Longitude coordinate of the place.
        owner_id (str): ID of the owner of the place.
        city (str): City where the place is located.
        country (str): Country where the place is located.
        is_available (bool): Availability status of the place.
        status (str): Status of the place (e.g., active, maintenance, blocked).
        minimum_stay (int): Minimum stay duration in nights.
        property_type (str): Type of the property
                            (e.g., house, apartment, villa).
        amenity_ids (list): List of amenity IDs associated with the place.
        review_ids (list): List of review IDs associated with the place.
    Methods:
        __init__: Initialize a new Place object.
        _validate_string: Validate string fields.
        _validate_positive_integer: Validate positive integer fields.
        _validate_positive_float: Validate positive float fields.
        _validate_latitude: Validate latitude.
        _validate_longitude: Validate longitude.
        _validate_status: Validate place status.
        _validate_property_type: Validate property type.
        _validate_bool: Validate boolean fields.
        filter_by_price: Filter places by price range.
        filter_by_capacity: Filter places by minimum guest capacity.
        get_by_location: Find places within a specific radius from coordinates.
        get_amenities: Get amenities for this place.
        get_reviews: Get reviews for this place.
        search: Search places based on multiple criteria.
        create: Create a new Place instance.
        update: Update Place instance attributes.
        add_amenity: Add an amenity to this place.
        remove_amenity: Remove an amenity from this place.
        to_dict: Convert Place instance to dictionary.'''
    repository = InMemoryRepository()

    @magic_wand(validate_input(PlaceValidation),
                validate_entity('User', 'owner_id'))
    def __init__(self, name, description, number_rooms, number_bathrooms,
                 max_guest, price_by_night, latitude, longitude, owner_id,
                 city="", country="", is_available=True, status='active',
                 minimum_stay=1, property_type='apartment', **kwargs):
        '''Initialize a new Place object.'''
        super().__init__(**kwargs)
        # Attributs
        self.name = self._validate_string(name, "name")
        self.description = self._validate_string(description, "description")
        self.number_rooms = self._validate_positive_integer(
            number_rooms, "number_rooms")
        self.number_bathrooms = self._validate_positive_integer(
            number_bathrooms, "number_bathrooms")
        self.max_guest = self._validate_positive_integer(
            max_guest, "max_guest")
        self.price_by_night = self._validate_positive_float(
            price_by_night, "price_by_night")
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.city = self._validate_string(city, "city")
        self.country = self._validate_string(country, "country")
        self.owner_id = self._validate_string(owner_id, "owner_id")
        self.is_available = self._validate_bool(is_available, "is_available")
        self.status = self._validate_status(status)
        self.minimum_stay = self._validate_positive_integer(
            minimum_stay, "minimum_stay")
        self.property_type = self._validate_property_type(property_type)

        # Lists
        self.amenity_ids = []
        self.review_ids = []

    @staticmethod
    @magic_wand()
    def _validate_string(value, field_name):
        '''Validate string fields.'''
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        return value.strip()

    @staticmethod
    @magic_wand()
    def _validate_positive_integer(value, field_name):
        '''Validate positive integer fields.'''
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
        '''Validate positive float.'''
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
        '''Validate latitude.'''
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
        '''Validate longitude.'''
        try:
            value = float(value)
            if not -180 <= value <= 180:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number between -180 and 180")
        return value

    @staticmethod
    @magic_wand()
    def _validate_status(value):
        """Validate place status."""
        valid_status = ['active', 'maintenance', 'blocked']
        if value not in valid_status:
            msg = f"Status must be one of: {', '.join(valid_status)}"
            raise ValueError(msg)
        return value

    @staticmethod
    @magic_wand()
    def _validate_property_type(value):
        """Validate property type."""
        valid_types = ['house', 'apartment', 'villa']
        if value not in valid_types:
            msg = f"Property type must be one of: {', '.join(valid_types)}"
            raise ValueError(msg)
        return value

    @staticmethod
    @magic_wand()
    def _validate_bool(value, field_name):
        """Validate boolean fields."""
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean")
        return value

    @classmethod
    @magic_wand(validate_input({'min_price': float, 'max_price': float}))
    def filter_by_price(cls, min_price: float,
                        max_price: float) -> List['Place']:
        """
        Filter places by price range.

        Args:
            min_price (float): Minimum price per night
            max_price (float): Maximum price per night

        Returns:
            List[Place]: Places within the price range
        """
        return [place for place in cls.get_all()
                if min_price <= place.price_by_night <= max_price]

    @classmethod
    @magic_wand(validate_input({'min_guests': int}))
    def filter_by_capacity(cls, min_guests: int) -> List['Place']:
        """
        Filter places by minimum guest capacity.

        Args:
            min_guests (int): Minimum number of guests

        Returns:
            List[Place]: Places with sufficient capacity
        """
        return [place for place in cls.get_all()
                if place.max_guest >= min_guests]

    @classmethod
    @magic_wand(validate_input({
        'latitude': float,
        'longitude': float,
        'radius': float
    }))
    def get_by_location(cls, latitude: float, longitude: float,
                        radius: float) -> List['Place']:
        """
        Find places within a specific radius from coordinates.

        Args:
            latitude (float): Center point latitude
            longitude (float): Center point longitude
            radius (float): Search radius in kilometers

        Returns:
            List[Place]: Places within the specified radius
        """
        def calculate_distance(lat1: float, lon1: float,
                               lat2: float, lon2: float) -> float:
            """Calculate distance between two points in kilometers."""
            R = 6371  # Earth's radius in km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2)**2 +
                 math.cos(math.radians(lat1)) *
                 math.cos(math.radians(lat2)) *
                 math.sin(dlon/2)**2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        return [place for place in cls.get_all()
                if calculate_distance(latitude, longitude,
                place.latitude, place.longitude) <= radius]

    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def get_amenities(self):
        '''Get amenities for this place.'''
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        place_amenities = PlaceAmenity.get_by_place(self.id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]

    @magic_wand(validate_entity('Review', 'review_id'), update_timestamp)
    def get_reviews(self):
        '''Get reviews for this place.'''
        from .review import Review
        return Review.get_by_place(self.id)

    @classmethod
    @magic_wand()
    def search(cls, **criteria) -> List['Place']:
        """Search places based on multiple criteria."""
        if not criteria:
            return cls.get_all()

        results = cls.get_all()
        for attr, value in criteria.items():
            if value is not None:
                results = [
                    place for place in results
                    if getattr(place, attr, None) == value
                ]
        return results

    @classmethod
    @magic_wand(validate_input(PlaceValidation),
                validate_entity(('User', 'owner_id')))
    def create(cls, **kwargs) -> 'Place':
        """
        Create a new Place instance.

        Args:
            **kwargs: Place attributes

        Returns:
            Place: New Place instance

        Raises:
            ValueError: If creation fails
        """
        place = cls(**kwargs)
        cls.repository.add(place)
        return place

    @magic_wand(validate_input(PlaceValidation),
                validate_entity(('User', 'owner_id')))
    def update(self, data: dict) -> 'Place':
        """Update Place instance attributes."""
        if 'owner_id' in data and data['owner_id'] != self.owner_id:
            raise ValueError("Cannot change owner_id")
        if 'amenity_ids' in data and not hasattr(self, 'amenity_ids'):
            self.amenity_ids = []
        if 'review_ids' in data and not hasattr(self, 'review_ids'):
            self.review_ids = []

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue

            if hasattr(self, f'_validate_{key}'):
                value = getattr(self, f'_validate_{key}')(value)
            elif key in ['number_rooms', 'number_bathrooms', 'max_guest']:
                value = self._validate_positive_integer(value, key)
            elif key == 'price_by_night':
                value = self._validate_positive_float(value, key)
            elif not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key}")

            setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)
        update_data = {k: getattr(self, k)
                       for k in data.keys() if hasattr(self, k)}
        update_data['updated_at'] = self.updated_at
        self.repository._storage[self.id] = self

        return self

    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def add_amenity(self, amenity):
        '''Add an amenity to this place.'''
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.create(place_id=self.id, amenity_id=amenity.id)

    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def remove_amenity(self, amenity):
        '''Remove an amenity from this place.'''
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.delete_by_place_and_amenity(self.id, amenity.id)

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """
        Convert Place instance to dictionary.

        Returns:
            dict: Place attributes dictionary
        """
        base_dict = super().to_dict()
        place_attributes = {
            'name', 'description', 'number_rooms', 'number_bathrooms',
            'max_guest', 'price_by_night', 'latitude', 'longitude',
            'owner_id', 'city', 'country', 'amenity_ids', 'review_ids',
            'is_available', 'status', 'minimum_stay', 'property_type'
        }

        return {
            **base_dict,
            **{attr: getattr(self, attr) for attr in place_attributes}
        }
