"""models module for the application."""
"""Initialize our haunted models! 👻."""
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity


__all__ = [
    "User",
    "Place",
    "Amenity",
    "Review",
    "PlaceAmenity"
]