# app/utils/model_validations.py
import datetime


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
    'country': (str, type(None))
}

AmenityValidation = {
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