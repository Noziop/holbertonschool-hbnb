from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity
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
    def create_user(self, user_data):
        return User.create(**user_data)

    @magic_wand(validate_input({'user_id': dict}), validate_entity('User', 'user_id'))
    def get_user(self, user_id):
        return User.get_by_id(user_id)


    @magic_wand(validate_input({'username': str}))
    def get_user_by_username(self, username):
        user = User.get_by_username(username)
        if not user:
            raise ValueError(f"No user found with username: {username}")
        return user

    @magic_wand(validate_input({'email': str}))
    def get_user_by_email(self, email):
        user = User.get_by_email(email)
        if not user:
            raise ValueError(f"No user found with email: {email}")
        return user

    @magic_wand(validate_input({'user_data': dict}, {'user_id': str}),
                validate_entity('User', 'user_id'))
    def update_user(self, user_id, user_data):
        user = User.get_by_id(user_id)
        user.update(user_data)
        return user

    def get_all_users(self):
        return User.get_all()

    @magic_wand(validate_input({'user_id': str, 'password': str}),
                validate_entity('User', 'user_id'))
    def check_user_password(self, user_id, password):
        user = User.get_by_id(user_id)
        return user.check_password(password)
    
    @magic_wand(validate_input({'user_id': str}),
            validate_entity('User', 'user_id'))
    def delete_user(self, user_id):
        user = User.get_by_id(user_id)
        if user:
            if user.delete():
                return True, f"User {user.username} (ID: {user_id}) deleted successfully"
        return False, f"User with ID {user_id} not found"

    # Place methods
    @magic_wand(validate_input({'place_data': dict}))
    def create_place(self, place_data):
        return Place.create(**place_data)

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_place(self, place_id):
        return Place.get_by_id(place_id)

    @magic_wand(validate_input({'place_id': str}, {'place_data': dict}),
                validate_entity('Place', 'place_id'))
    def update_place(self, place_id, place_data):
        place = Place.get_by_id(place_id)
        place.update(place_data)
        return place

    def get_all_places(self):
        return Place.get_all()

    @magic_wand(validate_input({'city': str}))
    def get_places_by_city(self, city):
        return Place.get_by_city(city)

    @magic_wand(validate_input({'country': str}))
    def get_places_by_country(self, country):
        return Place.get_by_country(country)

    @magic_wand(validate_input({'min_price': float}, {'max_price': float}))
    def get_places_by_price_range(self, min_price, max_price):
        return Place.get_by_price_range(min_price, max_price)

    @magic_wand(validate_input({'min_guests': int}))
    def get_places_by_capacity(self, min_guests):
        return Place.get_by_capacity(min_guests)

    @magic_wand(validate_input({'latitude': float}, {'longitude': float}, {'radius': float}))
    def get_places_by_location(self, latitude, longitude, radius):
        return Place.get_by_location(latitude, longitude, radius)

    @magic_wand(validate_input({'keywords': str}))
    def search_places(self, keywords):
        return Place.search(keywords)

    @magic_wand(validate_input({'place_id': str}), validate_entity('Place', 'place_id'))
    def get_place_amenities(self, place_id):
        place = Place.get_by_id(place_id)
        return place.get_amenities()

    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def add_amenity_to_place(self, place_id, amenity_id):
        place = Place.get_by_id(place_id)
        amenity = Amenity.get_by_id(amenity_id)
        place.add_amenity(amenity)

    @magic_wand(validate_input({'place_id': str}, {'amenity_id': str}),
                validate_entity('Place', 'place_id'),
                validate_entity('Amenity', 'amenity_id'))
    def remove_amenity_from_place(self, place_id, amenity_id):
        place = Place.get_by_id(place_id)
        amenity = Amenity.get_by_id(amenity_id)
        place.remove_amenity(amenity)

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_place_reviews(self, place_id):
        place = Place.get_by_id(place_id)
        return place.get_reviews()

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_place_details(self, place_id):
        place = Place.get_by_id(place_id)
        owner = User.get_by_id(place.owner_id)
        amenities = place.get_amenities()
        reviews = place.get_reviews()
        
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict()
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities]
        place_dict['reviews'] = [review.to_dict() for review in reviews]
        
        return place_dict

    # Review methods
    @magic_wand(validate_input({'review_data': dict}),
                validate_entity('Place', 'place_id'),
                validate_entity('User', 'user_id'))
    def create_review(self, review_data):
        return Review.create(**review_data)

    @magic_wand(validate_input({'review_id':str}), validate_entity('Review', 'review_id'))
    def get_review(self, review_id):
        return Review.get_by_id(review_id)

    @magic_wand(validate_input({'review_id':str}, {'review_data': dict}),
                validate_entity('Review', 'review_id'), update_timestamp)
    def update_review(self, review_id, review_data):
        review = Review.get_by_id(review_id)
        review.update(review_data)
        return review

    def get_all_reviews(self):
        return Review.get_all()

    @magic_wand(validate_input({'place_id': str}), validate_entity('Place', 'place_id'))
    def get_reviews_by_place(self, place_id):
        return Review.get_by_place(place_id)

    @magic_wand(validate_input({'user_id': str}), validate_entity('User', 'user_id'))
    def get_reviews_by_user(self, user_id):
        return Review.get_by_user(user_id)

    @magic_wand(validate_input({'review_id':str}),
                validate_entity('Review', 'review_id'), update_timestamp)
    def delete_review(self, review_id):
        review = Review.get_by_id(review_id)
        review.delete()

    @magic_wand(validate_input({'place_id': str}),
                validate_entity('Place', 'place_id'))
    def get_place_average_rating(self, place_id):
        reviews = self.get_reviews_by_place(place_id)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @magic_wand(validate_input({'limit': int}))
    def get_recent_reviews(self, limit=5):
        all_reviews = self.get_all_reviews()
        if not all_reviews:
            raise ValueError("No reviews found")
        return sorted(all_reviews, key=lambda x: x.created_at, reverse=True)[:limit]

    # Amenity methods
    @magic_wand(validate_input({'amenity_data':dict}))
    def create_amenity(self, amenity_data):
        return Amenity.create(**amenity_data)

    @magic_wand(validate_input({'amenity_id': str}), validate_entity('Amenity', 'amenity_id'))
    def get_amenity(self, amenity_id):
        return Amenity.get_by_id(amenity_id)

    @magic_wand(validate_input({'amenity_id': str}, {'amenity_data': dict}),
                validate_entity('Amenity', 'amenity_id'))
    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity.get_by_id(amenity_id)
        amenity.update(amenity_data)
        return amenity

    def get_all_amenities(self):
        return Amenity.get_all()

    @magic_wand(validate_input({'name': str}))
    def get_amenities_by_name(self, name):
        return Amenity.get_by_name(name)

    @magic_wand(validate_input({'keyword': str}))
    def search_amenities(self, keyword):
        return Amenity.search(keyword)

    @magic_wand(validate_input({'amenity_id': str}),
                validate_entity('Amenity', 'amenity_id'))
    def get_places_with_amenity(self, amenity_id):
        place_amenities = PlaceAmenity.get_by_amenity(amenity_id)
        if not place_amenities:
            raise ValueError(f"No places found with amenity id: {amenity_id}")
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
