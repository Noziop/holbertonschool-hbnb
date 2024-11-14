"""models module for the application."""

"""Initialize our haunted models! 👻."""
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity
from app.models.review import Review
from app.models.user import User

__all__ = ["User", "Place", "Amenity", "Review", "PlaceAmenity"]
