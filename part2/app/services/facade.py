from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity
from typing import List, Any, Tuple, Optional, Union
from datetime import datetime, timezone
from app.utils import *

class HBnBFacade:
    """The haunted gateway to our supernatural kingdom! 👻"""
    
    def __init__(self):
        """Summon our mystical repositories! 🔮"""
        self.user_repository = User.repository
        self.place_repository = Place.repository
        self.amenity_repository = Amenity.repository
        self.review_repository = Review.repository
        self.placeamenity_repository = PlaceAmenity.repository

    # === USER OPERATIONS === 👻
    @magic_wand(validate_input(UserValidation))
    def create_user(self, user_data: dict) -> User:
        """Summon a new spirit into our realm! 👻"""
        return User.create(**user_data)

    @magic_wand(validate_input({'user_id': str}))
    def get_user(self, user_id: str) -> User:
        """Find a spirit by their ethereal ID! 👻"""
        return User.get_by_id(user_id)

    @magic_wand(validate_input({'user_data': dict}))
    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update a spirit's manifestation! 🌟"""
        user = self.get_user(user_id)
        return user.update(user_data)

    @magic_wand(validate_input({'user_id': str}))
    def delete_user(self, user_id: str) -> bool:
        """Banish a spirit from our realm! ⚡"""
        user = self.get_user(user_id)
        return user.delete()

    @magic_wand()
    def find_users(self, **criteria) -> List[User]:
        """Search for spirits in our realm! 🔮"""
        return User.get_by_attr(multiple=True, **criteria)

    # Place methods
    @magic_wand(validate_input({'place_data': dict}))
    def create_place(self, place_data: dict) -> Place:
        """Create a new place. Home sweet home! 🏠"""
        return Place.create(**place_data)

    @magic_wand(validate_input({'place_id': str}))
    def get_place(self, place_id: str) -> Place:
        """Get place by ID. Finding that dream spot! ✨"""
        return Place.get_by_id(place_id)

    @magic_wand(validate_input({'attr': str, 'value': Any}))
    def get_places_by_attr(self, attr: str, value: Any) -> List[Place]:
        """Get places by any attribute. House hunting but make it fancy! 🔍"""
        return Place.repository.get_by_attribute(attr, value, multiple=True)

    @magic_wand(validate_input({'place_id': str, 'place_data': dict}))
    def update_place(self, place_id: str, place_data: dict) -> Place:
        """Update place. Renovation time! 🏗️"""
        place = Place.get_by_id(place_id)
        return place.update(place_data)

    @magic_wand(validate_input({'place_id': str}))
    def delete_place(self, place_id: str) -> Tuple[bool, str]:
        """Delete place. Moving out! 🚚"""
        place = Place.get_by_id(place_id)
        if place and place.delete():
            return True, f"Place {place.name} deleted successfully"
        return False, f"Place with ID {place_id} not found"

    @magic_wand()
    def get_all_places(self) -> List[Place]:
        """Get all places. The whole real estate portfolio! 🏘️"""
        return Place.get_all() or []

    @magic_wand(validate_input({'min_price': float, 'max_price': float}))
    def filter_by_price(self, min_price: float, max_price: float) -> List[Place]:
        """Find haunted houses within your budget! 💰"""
        return Place.filter_by_price(min_price, max_price)

    @magic_wand(validate_input({'latitude': float, 'longitude': float, 'radius': float}))
    def get_places_by_location(self, latitude: float, longitude: float, radius: float) -> List[Place]:
        """Get places by location. Location, location, location! 🌍"""
        return Place.get_by_location(latitude, longitude, radius)

    @magic_wand(validate_input({'keywords': str}))
    def search_places(self, keywords: str) -> List[Place]:
        """Search places. House hunting made fabulous! ✨"""
        return Place.search(keywords)

    # === REVIEW OPERATIONS === 📝
    @magic_wand(validate_input(ReviewValidation))
    def create_review(self, review_data: dict) -> Review:
        """Write a haunted review! Like Yelp for ghosts! 👻"""
        return Review.create(**review_data)

    @magic_wand(validate_input({'review_id': str}))
    def get_review(self, review_id: str) -> Review:
        """Find a specific spectral critique! 📜"""
        return Review.get_by_id(review_id)

    @magic_wand()
    def find_reviews(self, **criteria) -> List[Review]:
        """Search through our ghostly guestbook! 👻"""
        return Review.get_by_attr(multiple=True, **criteria)

    @magic_wand(validate_input({'place_id': str}))
    def get_place_reviews(self, place_id: str) -> List[Review]:
        """Read all the haunted tales about a place! 🏚️"""
        return Review.get_by_attr(multiple=True, place_id=place_id)

    @magic_wand(validate_input({'place_id': str}))
    def get_place_rating(self, place_id: str) -> float:
        """Calculate how haunted a place really is! 👻"""
        reviews = self.get_place_reviews(place_id)
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)

    @magic_wand(validate_input({'review_id': str, 'review_data': dict}))
    def update_review(self, review_id: str, review_data: dict) -> Review:
        """Update a ghostly critique! 📝"""
        review = self.get_review(review_id)
        return review.update(review_data)

    @magic_wand(validate_input({'review_id': str}),
                validate_entity('Review', 'review_id'))
    def delete_review(self, review_id: str) -> bool:
        """Make a review disappear like a ghost! 👻"""
        review = self.get_review(review_id)
        return review.delete()

    @magic_wand(validate_input({'limit': int}))
    def get_recent_reviews(self, limit: int = 5) -> List[Review]:
        """Get the freshest haunted tales! 🆕"""
        all_reviews = self.find_reviews()
        return sorted(all_reviews, 
                     key=lambda x: x.created_at, 
                     reverse=True)[:limit]

    # === AMENITY OPERATIONS === ✨
    @magic_wand(validate_input(AmenityValidation))
    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Add a new supernatural feature! Phone home included! 👽📱"""
        return Amenity.create(**amenity_data)

    @magic_wand(validate_input({'amenity_id': str}))
    def get_amenity(self, amenity_id: str) -> Amenity:
        """Find a specific haunted feature! 🔍"""
        return Amenity.get_by_id(amenity_id)

    @magic_wand()
    def find_amenities(self, **criteria) -> List[Amenity]:
        """Browse our catalog of supernatural features! 👻"""
        return Amenity.get_by_attr(multiple=True, **criteria)

    @magic_wand(validate_input({'amenity_id': str, 'amenity_data': dict}))
    def update_amenity(self, amenity_id: str, amenity_data: dict) -> Amenity:
        """Upgrade a spectral feature! Even ET needs updates! 🛸"""
        amenity = self.get_amenity(amenity_id)
        return amenity.update(amenity_data)

    @magic_wand(validate_input({'amenity_id': str}))
    def delete_amenity(self, amenity_id: str) -> bool:
        """Remove a feature. ET go home! 👋"""
        amenity = self.get_amenity(amenity_id)
        return amenity.delete()

    @magic_wand(validate_input({'place_id': str, 'amenity_id': str}))
    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> PlaceAmenity:
        """Install a new feature. Like adding a phone to call home! 📞"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        return PlaceAmenity.create(place_id=place.id, amenity_id=amenity.id)

    # === PLACE-AMENITY OPERATIONS === 🏚️✨
    @magic_wand(validate_input({'place_id': str, 'amenity_id': str}))
    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> PlaceAmenity:
        """Install a haunted feature! Like adding a Ouija board to a séance! 🔮"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        return PlaceAmenity.create(place_id=place.id, amenity_id=amenity.id)

    @magic_wand(validate_input({'place_id': str}))
    def get_place_amenities(self, place_id: str) -> List[Amenity]:
        """See what supernatural features haunt this place! 👻"""
        place = self.get_place(place_id)  # Vérifie que la place existe
        place_amenities = PlaceAmenity.get_by_attr(multiple=True, place_id=place_id)
        return [self.get_amenity(pa.amenity_id) for pa in place_amenities]

    @magic_wand(validate_input({'amenity_id': str}))
    def get_places_with_amenity(self, amenity_id: str) -> List[Place]:
        """Find all places haunted by this feature! 🏚️"""
        amenity = self.get_amenity(amenity_id)  # Vérifie que l'amenity existe
        place_amenities = PlaceAmenity.get_by_attr(multiple=True, amenity_id=amenity_id)
        return [self.get_place(pa.place_id) for pa in place_amenities]

    @magic_wand(validate_input({'place_id': str, 'amenity_id': str}))
    def remove_amenity_from_place(self, place_id: str, amenity_id: str) -> bool:
        """Exorcise a feature from a place! ⚡"""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        return PlaceAmenity.delete_by_place_and_amenity(place.id, amenity.id)