"""Module for Place class - Where haunted houses come to life! 👻"""
from typing import List, Dict, Any
from datetime import datetime, timezone
import math
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class Place(BaseModel):
    """
    Place Model: The haunted mansion of our dreams! 🏚️
    Where every room has a story, and every amenity might be possessed!
    """
    repository = InMemoryRepository()
    
    # Validation constants to keep our spirits organized! 👻
    VALID_STATUS = ['active', 'maintenance', 'blocked']
    VALID_TYPES = ['house', 'apartment', 'villa']
    
    @magic_wand(validate_input(PlaceValidation),
                validate_entity('User', 'owner_id'))
    def __init__(self, name: str, description: str, **kwargs) -> None:
        """Summon a new haunted place into existence! 🏚️"""
        super().__init__(**kwargs)
        
        # Validate and set all our cursed attributes! 🧙‍♀️
        validators = {
            'name': self._validate_string,
            'description': self._validate_string,
            'number_rooms': self._validate_positive_integer,
            'number_bathrooms': self._validate_positive_integer,
            'max_guest': self._validate_positive_integer,
            'price_by_night': self._validate_positive_float,
            'latitude': self._validate_latitude,
            'longitude': self._validate_longitude,
            'city': self._validate_string,
            'country': self._validate_string,
            'owner_id': self._validate_string,
            'is_available': self._validate_bool,
            'status': self._validate_status,
            'minimum_stay': self._validate_positive_integer,
            'property_type': self._validate_property_type
        }
        
        # Set default values for our haunted mansion! 👻
        defaults = {
            'city': "",
            'country': "",
            'is_available': True,
            'status': 'active',
            'minimum_stay': 1,
            'property_type': 'apartment'
        }
        
        # Merge kwargs with defaults
        data = {**defaults, **kwargs, 'name': name, 'description': description}
        
        # Validate and set all attributes
        for attr, validator in validators.items():
            if attr in data:
                setattr(self, attr, validator(data[attr], attr))
        
        # Initialize our ghostly lists
        self.amenity_ids = []
        self.review_ids = []

    @staticmethod
    @magic_wand()
    def _validate_string(value, field_name):
        """Validate strings like a grammar ghost! 📚👻"""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string, darling! Not your dating history! 💅")
        return value.strip()

    @staticmethod
    @magic_wand()
    def _validate_positive_integer(value, field_name):
        """Count like a vampire counts his victims! 🧛‍♀️"""
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be positive! Like our spirits! ✨")
        return value

    @staticmethod
    @magic_wand()
    def _validate_positive_float(value, field_name):
        """Float like a ghost through walls! 👻"""
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} must be a positive number, like our energy! 💫")
        return value

    @staticmethod
    @magic_wand()
    def _validate_latitude(value, field_name=None) -> float:
        """
        Validate latitude like a ghost's vertical haunting range! 👻
        
        Args:
            value: The latitude to validate
            field_name: Optional field name for error messages
        """
        try:
            value = float(value)
            if not -90 <= value <= 90:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Latitude must be between -90 and 90, like a ghost's dance range! 👻")
        return value

    @staticmethod
    @magic_wand()
    def _validate_longitude(value, field_name=None) -> float:
        """
        Validate longitude like a ghost's horizontal haunting range! 👻
        
        Args:
            value: The longitude to validate
            field_name: Optional field name for error messages
        """
        try:
            value = float(value)
            if not -180 <= value <= 180:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Longitude must be between -180 and 180, like a spirit's travel limits! 👻")
        return value

    @staticmethod
    @magic_wand()
    def _validate_status(value, field_name=None):
        """Check status like a ghost checks their haunting schedule! 👻"""
        valid_status = ['active', 'maintenance', 'blocked']
        if value not in valid_status:
            msg = f"Status must be one of: {', '.join(valid_status)}. Even ghosts need organization! 📋"
            raise ValueError(msg)
        return value

    @staticmethod
    @magic_wand()
    def _validate_property_type(value, field_name=None):
        """Validate property type like a ghost choosing their haunt! 🏚️"""
        valid_types = ['house', 'apartment', 'villa']
        if value not in valid_types:
            msg = f"Property type must be one of: {', '.join(valid_types)}. We're picky spirits! 👻"
            raise ValueError(msg)
        return value

    @staticmethod
    @magic_wand()
    def _validate_bool(value, field_name):
        """Check booleans like a ghost checks if they're visible! 👻"""
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean! True or False, no ghosting! 👻")
        return value

    @classmethod
    @magic_wand(validate_input({'min_price': float, 'max_price': float}))
    def filter_by_price(cls, min_price: float, max_price: float) -> List['Place']:
        """
        Filter places by price range like a ghost hunting for bargains! 💰
        
        Args:
            min_price: The minimum price (even spirits have budgets! 👻)
            max_price: The maximum price (we're dead, not made of money! 💸)
        
        Returns:
            List of haunted places that won't break your spiritual bank! 🏚️
        """
        return [place for place in cls.get_all()
                if min_price <= place.price_by_night <= max_price]

    @classmethod
    @magic_wand(validate_input({'min_guests': int}))
    def filter_by_capacity(cls, min_guests: int) -> List['Place']:
        """
        Filter places by capacity like planning a ghost party! 👻
        
        Args:
            min_guests: Minimum spirits that can haunt at once! 👻👻👻
        
        Returns:
            List of places ready for your supernatural soirée! 🎃
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
        Find haunted places nearby like a supernatural GPS! 🗺️
        
        Args:
            latitude: Your ghostly latitude (even spirits need coordinates! 👻)
            longitude: Your spooky longitude (haunting has gone digital! 💫)
            radius: How far your spirit is willing to float! 👻
        
        Returns:
            List of places within haunting distance! 🏚️
        """
        def calculate_distance(lat1: float, lon1: float,
                            lat2: float, lon2: float) -> float:
            """Calculate distance like measuring ghost trails! 👻"""
            R = 6371  # Earth's radius (or as we call it, the Ghost Globe! 🌍)
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
    def get_amenities(self) -> List['Amenity']:
        """
        Get all supernatural features of this haunted place! 👻
        
        Returns:
            List of cursed amenities that make this place spooktacular! 🦇
        """
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        place_amenities = PlaceAmenity.get_by_attr(multiple=True, place_id=self.id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]

    @classmethod
    @magic_wand(validate_input(PlaceValidation),
                validate_entity(('User', 'owner_id')))
    def create(cls, **kwargs) -> 'Place':
        """
        Summon a new haunted place into existence! 🏚️
        
        Args:
            **kwargs: The dark ingredients for our haunted creation! 🧪
        
        Returns:
            A newly possessed Place, ready for haunting! 👻
        
        Raises:
            ValueError: When the spirits reject our offering! 💀
        """
        place = cls(**kwargs)
        cls.repository.add(place)
        return place

    @magic_wand(validate_input(PlaceValidation),
                validate_entity(('User', 'owner_id')))
    def update(self, data: dict) -> 'Place':
        """
        Update this cursed dwelling! Like supernatural renovation! 🏚️
        
        Raises:
            ValueError: When the spirits refuse our changes! 
            The ghosts are picky about their home decor! 👻
        """
        if 'owner_id' in data and data['owner_id'] != self.owner_id:
            raise ValueError("Cannot change owner_id - Ghosts are loyal to their master! 👻")
        
        # Initialize our cursed collections if they don't exist
        for collection in ['amenity_ids', 'review_ids']:
            if collection in data and not hasattr(self, collection):
                setattr(self, collection, [])

        # Update our haunted attributes
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue  # Some things are sacred, even for ghosts! ✨

            if hasattr(self, f'_validate_{key}'):
                value = getattr(self, f'_validate_{key}')(value)
            elif key in ['number_rooms', 'number_bathrooms', 'max_guest']:
                value = self._validate_positive_integer(value, key)
            elif key == 'price_by_night':
                value = self._validate_positive_float(value, key)
            elif not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key} - The spirits don't recognize this! 👻")

            setattr(self, key, value)

        # Mark the time of this supernatural transformation
        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def add_amenity(self, amenity):
        """Add a supernatural feature to this haunted place! ✨"""
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.create(place_id=self.id, amenity_id=amenity.id)

    @magic_wand(validate_entity('Amenity', 'amenity_id'))
    def remove_amenity(self, amenity):
        """Exorcise an amenity from this cursed dwelling! 🕯️"""
        from .placeamenity import PlaceAmenity
        from .amenity import Amenity
        PlaceAmenity.delete_by_place_and_amenity(self.id, amenity.id)

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """
        Transform this haunted place into mortal-readable format! 📜
        Like writing in a ghost diary, but more structured! ✨
        
        Returns:
            A spooky dictionary of our supernatural dwelling! 🏚️
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
