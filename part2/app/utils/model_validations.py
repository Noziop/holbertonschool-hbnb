# app/utils/model_validations.py
from datetime import datetime

#Dictionary to validate an attribute of type a model
BaseModelValidation = {
    'id': str,
    'created_at': datetime,
    'updated_at': datetime
}

UserValidation = {
    'username': str,
    'email': str,
    'password': str,
    'first_name': str,
    'last_name': str,
    'phone_number': (str, type(None))
}

PlaceValidation = {
    'name': str,
    'description': str,
    'number_rooms': int,
    'number_bathrooms': int,
    'max_guest': int,
    'price_by_night': float,
    'latitude': float,
    'longitude': float,
    'owner_id': str,
    'city': (str, type(None)),
    'country': (str, type(None)),
    'is_available': bool,
    'status': str,
    'minimum_stay': int,
    'property_type': str
}

AmenityValidation = {
    'amenity_id': str,
    'name': str
}

ReviewValidation = {
    'place_id': str,
    'user_id': str,
    'text': str,
    'rating': int,
    'limit': int
}

PlaceAmenityValidation = {
    'place_id': str,
    'amenity_id': str
}

#Dictionary to validate an attribute of a model exists in persistence

BaseEntityValidation = {
    'id': 'BaseModel',
    'created_at': 'BaseModel',
    'updated_at': 'BaseModel',
}
UserEntityValidation = {
    'user_id': 'User',
    'username': 'User',
    'email': 'User',
    'password': 'User',
    'first_name': 'User',
    'last_name': 'User',
    'phone_number': 'User',
}
PlaceEntityValidation = {
    'place_id': 'Place',
    'name': 'Place',
    'description': 'Place',
    'number_rooms': 'Place',
    'number_bathrooms': 'Place',
    'max_guest': 'Place',
    'price_by_night': 'Place',
    'latitude': 'Place',
    'longitude': 'Place',
    'owner_id': 'Place',
    'city': 'Place',
    'country': 'Place',
    'is_available': 'Place',
    'status': 'Place',
    'minimum_stay': 'Place',
    'property_type': 'Place'
}
AmenityEntityValidation = {
    'amenity_id': 'Amenity',
    'name': 'Amenity',
}
ReviewEntityValidation = {
    'review_id': 'Review',
    'place_id': 'Review',
    'user_id': 'Review',
    'text': 'Review',
    'rating': 'Review'
}

PlaceAmenityValidation = {
    'place_id': str,
    'amenity_id': str
}