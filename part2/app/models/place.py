# app/models/place.py
"""Place model module: Where haunted houses come to life! 👻"""
from typing import Optional, Dict, Any, List, TYPE_CHECKING
import re
import math
from app.models.basemodel import BaseModel

# Conditional imports for type hints
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.review import Review
    from app.models.amenity import Amenity

class Place(BaseModel):
    """Place: A haunted location in our supernatural realm! 🏰"""
    
    # Validation constants
    VALID_STATUS = ['active', 'maintenance', 'blocked']
    VALID_TYPES = ['house', 'apartment', 'villa']
    
    def __init__(
        self,
        name: str,
        description: str,
        owner_id: str,
        price_by_night: float,
        number_rooms: int = 1,
        number_bathrooms: int = 1,
        max_guest: int = 2,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        city: Optional[str] = "",
        country: Optional[str] = "",
        status: str = 'active',
        property_type: str = 'apartment',
        minimum_stay: int = 1,
        **kwargs
    ):
        """Initialize a new haunted place! ✨"""
        self.logger.debug(f"Creating new Place with name: {name}")
        super().__init__(**kwargs)
        
        # Required attributes
        self.name = self._validate_name(name)
        self.description = self._validate_description(description)
        self.owner_id = self._validate_owner_id(owner_id)
        self.price_by_night = self._validate_price(price_by_night)
        
        # Optional attributes with defaults
        self.number_rooms = self._validate_positive_integer(number_rooms, "number_rooms")
        self.number_bathrooms = self._validate_positive_integer(number_bathrooms, "number_bathrooms")
        self.max_guest = self._validate_positive_integer(max_guest, "max_guest")
        self.latitude = self._validate_latitude(latitude) if latitude else None
        self.longitude = self._validate_longitude(longitude) if longitude else None
        self.city = city
        self.country = country
        self.status = self._validate_status(status)
        self.property_type = self._validate_property_type(property_type)
        self.minimum_stay = self._validate_positive_integer(minimum_stay, "minimum_stay")
        
        self.logger.info(f"Created new Place with ID: {self.id}")

    def _validate_name(self, name: str) -> str:
        """Validate place name! 🏰"""
        self.logger.debug(f"Validating place name: {name}")
        if not isinstance(name, str) or len(name.strip()) < 3:
            error_msg = "Name must be at least 3 characters!"
            self.logger.error(f"Name validation failed: {error_msg}")
            raise ValueError(error_msg)
        return name.strip()

    def _validate_description(self, description: str) -> str:
        """Validate place description! 📝"""
        self.logger.debug(f"Validating place description")
        if not isinstance(description, str) or len(description.strip()) < 10:
            error_msg = "Description must be at least 10 characters!"
            self.logger.error(f"Description validation failed: {error_msg}")
            raise ValueError(error_msg)
        return description.strip()

    def _validate_owner_id(self, owner_id: str) -> str:
        """Validate owner ID! 👤"""
        self.logger.debug(f"Validating owner ID: {owner_id}")
        if not isinstance(owner_id, str):
            error_msg = "Owner ID must be a string!"
            self.logger.error(f"Owner ID validation failed: {error_msg}")
            raise ValueError(error_msg)
        return owner_id

    def _validate_price(self, price: float) -> float:
        """Validate price! 💰"""
        self.logger.debug(f"Validating price: {price}")
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Price must be a positive number!"
            self.logger.error(f"Price validation failed: {error_msg}")
            raise ValueError(error_msg)
        return price

    def _validate_positive_integer(self, value: int, field: str) -> int:
        """Validate positive integer! 🔢"""
        self.logger.debug(f"Validating {field}: {value}")
        try:
            value = int(value)
            if value <= 0:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = f"{field} must be a positive integer!"
            self.logger.error(f"Integer validation failed: {error_msg}")
            raise ValueError(error_msg)
        return value

    def _validate_latitude(self, latitude: float) -> float:
        """Validate latitude! 🌍"""
        self.logger.debug(f"Validating latitude: {latitude}")
        try:
            latitude = float(latitude)
            if not -90 <= latitude <= 90:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Latitude must be between -90 and 90!"
            self.logger.error(f"Latitude validation failed: {error_msg}")
            raise ValueError(error_msg)
        return latitude

    def _validate_longitude(self, longitude: float) -> float:
        """Validate longitude! 🌍"""
        self.logger.debug(f"Validating longitude: {longitude}")
        try:
            longitude = float(longitude)
            if not -180 <= longitude <= 180:
                raise ValueError
        except (ValueError, TypeError):
            error_msg = "Longitude must be between -180 and 180!"
            self.logger.error(f"Longitude validation failed: {error_msg}")
            raise ValueError(error_msg)
        return longitude

    def _validate_status(self, status: str) -> str:
        """Validate place status! 📊"""
        self.logger.debug(f"Validating status: {status}")
        if status not in self.VALID_STATUS:
            error_msg = f"Status must be one of: {', '.join(self.VALID_STATUS)}"
            self.logger.error(f"Status validation failed: {error_msg}")
            raise ValueError(error_msg)
        return status

    def _validate_property_type(self, property_type: str) -> str:
        """Validate property type! 🏠"""
        self.logger.debug(f"Validating property type: {property_type}")
        if property_type not in self.VALID_TYPES:
            error_msg = f"Property type must be one of: {', '.join(self.VALID_TYPES)}"
            self.logger.error(f"Property type validation failed: {error_msg}")
            raise ValueError(error_msg)
        return property_type

    def update(self, data: dict) -> 'Place':
        """Update place attributes! 🏰"""
        self.logger.debug(f"Attempting to update Place: {self.id}")
        try:
            # Validate new values before update
            if 'name' in data:
                data['name'] = self._validate_name(data['name'])
            if 'description' in data:
                data['description'] = self._validate_description(data['description'])
            if 'price_by_night' in data:
                data['price_by_night'] = self._validate_price(data['price_by_night'])
            if 'status' in data:
                data['status'] = self._validate_status(data['status'])
            if 'property_type' in data:
                data['property_type'] = self._validate_property_type(data['property_type'])
            
            return super().update(data)
        except Exception as e:
            self.logger.error(f"Failed to update Place: {str(e)}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """Transform place into dictionary! 📚"""
        self.logger.debug(f"Converting place {self.id} to dictionary")
        base_dict = super().to_dict()
        place_dict = {
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'price_by_night': self.price_by_night,
            'number_rooms': self.number_rooms,
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'city': self.city,
            'country': self.country,
            'status': self.status,
            'property_type': self.property_type,
            'minimum_stay': self.minimum_stay
        }
        return {**base_dict, **place_dict}