from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity
from typing import List, Any, Tuple, Optional, Union
from datetime import datetime, timezone
from app.utils import *

class HBnBFacade:
    def __init__(self):
        self.user_repository = User.repository
        self.place_repository = Place.repository
        self.amenity_repository = Amenity.repository
        self.review_repository = Review.repository
        self.placeamenity_repository = PlaceAmenity.repository

    # User methods
    @magic_wand(validate_input(UserValidation))
    def create_user(self, user_data: dict) -> User:
        """Create a new user. Birth of a queen! 👑"""
        return User.create(**user_data)

    @magic_wand(validate_input({'user_id': str}))
    def get_user(self, user_id: str) -> User:
        """Get user by ID. Finding that special someone! 💫"""
        return User.get_by_id(user_id)

    @magic_wand(validate_input({'attr': str, 'value': str}))
    def get_user_by_attr(self, attr: str, value: str) -> User:
        """Get user by any attribute. Like finding the perfect match! 💘"""
        user = User.repository.get_by_attribute(attr, value)
        if not user:
            raise ValueError(f"No user found with {attr}: {value}")
        return user

    @magic_wand(validate_input({'user_id': str, 'user_data': dict}))
    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update user. Glow up time! ✨"""
        user = User.get_by_id(user_id)
        return user.update(user_data)

    @magic_wand()
    def get_all_users(self) -> List[User]:
        """Get all users. The whole squad! 💃"""
        return User.get_all()

    @magic_wand(validate_input({'user_id': str, 'password': str}))
    def check_user_password(self, user_id: str, password: str) -> bool:
        """Check user password. No peeking! 🙈"""
        user = User.get_by_id(user_id)
        return user.check_password(password)

    @magic_wand(validate_input({'user_id': str}))
    def delete_user(self, user_id: str) -> Tuple[bool, str]:
        """Delete user. Bye Felicia! 👋"""
        user = User.get_by_id(user_id)
        if user and user.delete():
            return True, f"User {user.username} deleted successfully"
        return False, f"User with ID {user_id} not found"

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
    def get_places_by_price_range(self, min_price: float, max_price: float) -> List[Place]:
        """Get places by price range. Shopping with style! 💰"""
        return Place.get_by_price_range(min_price, max_price)

    @magic_wand(validate_input({'latitude': float, 'longitude': float, 'radius': float}))
    def get_places_by_location(self, latitude: float, longitude: float, radius: float) -> List[Place]:
        """Get places by location. Location, location, location! 🌍"""
        return Place.get_by_location(latitude, longitude, radius)

    @magic_wand(validate_input({'keywords': str}))
    def search_places(self, keywords: str) -> List[Place]:
        """Search places. House hunting made fabulous! ✨"""
        return Place.search(keywords)

    # Review methods
    @magic_wand(validate_input({'review_data': dict}))
    def create_review(self, review_data: dict) -> Review:
        """Create a review. Time to spill the tea! ☕"""
        return Review.create(**review_data)

    @magic_wand(validate_input({'review_id': str}))
    def get_review(self, review_id: str) -> Review:
        """Get review by ID. Reading the receipts! 📝"""
        return Review.get_by_id(review_id)

    @magic_wand(validate_input({'attr': str, 'value': Any}))
    def get_reviews_by_attr(self, attr: str, value: Any) -> List[Review]:
        """Get reviews by any attribute. Gossip central! 💅"""
        return Review.repository.get_by_attribute(attr, value, multiple=True)

    @magic_wand(validate_input({'review_id': str, 'review_data': dict}))
    def update_review(self, review_id: str, review_data: dict) -> Review:
        """Update review. Changed your mind? We got you! 💭"""
        review = Review.get_by_id(review_id)
        return review.update(review_data)

    @magic_wand(validate_input({'review_id': str}))
    def delete_review(self, review_id: str) -> Tuple[bool, str]:
        """Delete review. Taking it back! ⏪"""
        review = Review.get_by_id(review_id)
        if review and review.delete():
            return True, f"Review deleted successfully"
        return False, f"Review with ID {review_id} not found"

    @magic_wand()
    def get_all_reviews(self) -> List[Review]:
        """Get all reviews. All the tea, all the time! 🫖"""
        return Review.get_all() or []

    @magic_wand(validate_input({'place_id': str}))
    def get_place_average_rating(self, place_id: str) -> float:
        """Get place average rating. The tea-meter! 📊"""
        reviews = self.get_reviews_by_attr('place_id', place_id)
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)

    @magic_wand(validate_input({'limit': int}))
    def get_recent_reviews(self, limit: int = 5) -> List[Review]:
        """Get recent reviews. Fresh tea, honey! 🍵"""
        reviews = self.get_all_reviews()
        if not reviews:
            return []
        return sorted(reviews, key=lambda x: x.created_at, reverse=True)[:limit]

    # Amenity methods
    @magic_wand(validate_input({'amenity_data': dict}))
    def create_amenity(self, amenity_data: dict) -> Amenity:
        """Create amenity. Adding some spice to life! ✨"""
        return Amenity.create(**amenity_data)

    @magic_wand(validate_input({'amenity_id': str}))
    def get_amenity(self, amenity_id: str) -> Amenity:
        """Get amenity by ID. Finding that special feature! 🎯"""
        return Amenity.get_by_id(amenity_id)

    @magic_wand(validate_input({'attr': str, 'value': Any}))
    def get_amenities_by_attr(self, attr: str, value: Any) -> List[Amenity]:
        """Get amenities by any attribute. Shopping for features! 🛍️"""
        return Amenity.repository.get_by_attribute(attr, value, multiple=True)

    @magic_wand(validate_input({'amenity_id': str, 'amenity_data': dict}))
    def update_amenity(self, amenity_id: str, amenity_data: dict) -> tuple[bool, str, Optional[Amenity]]:
        """Update amenity. Upgrade time! 🔄"""
        try:
            amenity = Amenity.get_by_id(amenity_id)
            if not amenity:
                return False, "Amenity not found", None
            amenity.update(amenity_data)
            return True, "Amenity updated successfully", amenity
        except ValueError as e:
            raise ValueError(f"Failed to update amenity: {str(e)}")

    @magic_wand(validate_input({'amenity_id': str}))
    def delete_amenity(self, amenity_id: str) -> tuple[bool, str]:
        """Delete amenity. Decluttering with style! 🧹"""
        amenity = Amenity.get_by_id(amenity_id)
        if amenity and amenity.delete():
            return True, f"Amenity {amenity.name} deleted successfully"
        return False, f"Amenity with ID {amenity_id} not found"

    @magic_wand()
    def get_all_amenities(self) -> List[Amenity]:
        """Get all amenities. Feature parade! ✨"""
        return Amenity.get_all() or []

    @magic_wand(validate_input({'keyword': str}))
    def search_amenities(self, keyword: str) -> List[Amenity]:
        """Search amenities. Feature hunting! 🔍"""
        return Amenity.search(keyword)

    @magic_wand(validate_input({'amenity_id': str}))
    def get_places_with_amenity(self, amenity_id: str) -> List[Place]:
        """Get places with specific amenity. Match made in heaven! 💘"""
        place_amenities = PlaceAmenity.repository.get_by_attribute('amenity_id', amenity_id, multiple=True)
        if not place_amenities:
            return []
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    # PlaceAmenity methods
    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}))
    def create_place_amenity(self, place_id, amenity_id):
        place = Place.get_by_id(place_id) or Place.get_by_name(place_id)
        if not place:
            raise ValueError(f"No place found with id or name: {place_id}")
        
        amenity = Amenity.get_by_id(amenity_id) or Amenity.get_by_name(amenity_id)
        if not amenity:
            raise ValueError(f"No amenity found with id or name: {amenity_id}")
        
        return PlaceAmenity.create(place_id=place.id, amenity_id=amenity.id)

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_place_amenities(self, place_id):
        return PlaceAmenity.get_by_place(place_id)

    @magic_wand(validate_input({'amenity_id': str}),
                validate_entity('Amenity', 'amenity_id'))
    def get_amenity_places(self, amenity_id):
        return PlaceAmenity.get_by_amenity(amenity_id)

    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def delete_place_amenity(self, place_id, amenity_id):
        try:
            place_amenities = PlaceAmenity.get_by_place(place_id)
            if not place_amenities:
                raise ValueError(f"No PlaceAmenity found for place_id {place_id}")
            for pa in place_amenities:
                if pa.amenity_id == amenity_id:
                    pa.delete()
                    return
        except ValueError as e:
            raise ValueError(f"No PlaceAmenity found for place_id {place_id} and amenity_id {amenity_id}")

    # Méthode pour obtenir tous les aménités d'un lieu
    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_amenities_for_place(self, place_id):
        try:
            place = self.get_place(place_id)  # This will raise ValueError if place doesn't exist
            place_amenities = self.get_place_amenities(place_id)
            return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]
        except ValueError as e:
            raise ValueError(f"Failed to get amenities for {place}: {str(e)}")
        
    # Méthode pour ajouter un aménité à un lieu
    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def add_amenity_to_place(self, place_id, amenity_id):
        try:
            place = Place.get_by_id(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            
            amenity = Amenity.get_by_id(amenity_id)
            if not amenity:
                raise ValueError(f"No amenity found with id: {amenity_id}")
            
            existing = PlaceAmenity.get_by_place_and_amenity(place_id, amenity_id)
            if existing:
                return existing  # L'association existe déjà, on la retourne
            
            return PlaceAmenity.create(place_id=place_id, amenity_id=amenity_id)
        except ValueError as e:
            raise ValueError(f"Failed to add {amenity.name if amenity else 'amenity'} to {place.name if place else 'place'}: {str(e)}")

    # Méthode pour retirer un aménité d'un lieu
    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'), update_timestamp)
    def remove_amenity_from_place(self, place_id, amenity_id):
        try:
            self.delete_place_amenity(place_id, amenity_id)
        except ValueError as e: 
            raise ValueError(f"Failed to remove amenity from place: {str(e)}")
        
    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'), update_timestamp)
    def delete_place_amenity(self, place_id, amenity_id):
        place_amenities = PlaceAmenity.get_by_place(place_id)
        if not place_amenities:
            raise ValueError(f"No PlaceAmenity found for place_id {place_id}")
        for pa in place_amenities:
            if pa.amenity_id == amenity_id:
                pa.delete()
                return
        raise ValueError(f"No PlaceAmenity found for place_id {place_id} and amenity_id {amenity_id}")

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_amenities_for_place(self, place_id):
        place = self.get_place(place_id)
        place_amenities = self.get_place_amenities(place_id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]

    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def add_amenity_to_place(self, place_id, amenity_id):
        place = Place.get_by_id(place_id)
        amenity = Amenity.get_by_id(amenity_id)
        existing = PlaceAmenity.get_by_place_and_amenity(place_id, amenity_id)
        if existing:
            return existing  # L'association existe déjà, on la retourne
        return PlaceAmenity.create(place_id=place_id, amenity_id=amenity_id)

    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def remove_amenity_from_place(self, place_id, amenity_id):
        self.delete_place_amenity(place_id, amenity_id)
