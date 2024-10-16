from app.models.user import User
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = User.repository
        self.place_repository = Place.repository
        # Initialiser d'autres repositories si nécessaire

    # User methods
    def create_user(self, user_data):
        try:
            return User.create(**user_data)
        except ValueError as e:
            raise ValueError(f"Failed to create user: {str(e)}")

    def get_user(self, user_id):
        try:
            return User.get_by_id(user_id)
        except ValueError as e:
            raise ValueError(f"Failed to get user: {str(e)}")

    def get_user_by_username(self, username):
        user = User.get_by_username(username)
        if not user:
            raise ValueError(f"No user found with username: {username}")
        return user

    def get_user_by_email(self, email):
        user = User.get_by_email(email)
        if not user:
            raise ValueError(f"No user found with email: {email}")
        return user

    def update_user(self, user_id, user_data):
        try:
            user = self.get_user(user_id)
            user.update(user_data)
            return user
        except ValueError as e:
            raise ValueError(f"Failed to update user: {str(e)}")

    def get_all_users(self):
        return User.get_all()

    def check_user_password(self, user_id, password):
        try:
            user = self.get_user(user_id)
            return user.check_password(password)
        except ValueError as e:
            raise ValueError(f"Failed to check password: {str(e)}")

    # Méthodes pour Place
    def create_place(self, place_data):
        try:
            return Place.create(**place_data)
        except ValueError as e:
            raise ValueError(f"Failed to create place: {str(e)}")

    def get_place(self, place_id):
        try:
            return Place.get_by_id(place_id)
        except ValueError as e:
            raise ValueError(f"Failed to get place: {str(e)}")

    def update_place(self, place_id, place_data):
        try:
            place = self.get_place(place_id)
            place.update(place_data)
            return place
        except ValueError as e:
            raise ValueError(f"Failed to update place: {str(e)}")

    def get_all_places(self):
        return Place.get_all()

    def get_places_by_city(self, city):
        return Place.get_by_city(city)

    def get_places_by_country(self, country):
        return Place.get_by_country(country)

    def get_places_by_price_range(self, min_price, max_price):
        return Place.get_by_price_range(min_price, max_price)

    def get_places_by_capacity(self, min_guests):
        return Place.get_by_capacity(min_guests)

    def get_places_by_location(self, latitude, longitude, radius):
        return Place.get_by_location(latitude, longitude, radius)

    def search_places(self, keywords):
        return Place.search(keywords)

    def get_place_amenities(self, place_id):
        place = self.get_place(place_id)
        return place.get_amenities()

    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = Amenity.get_by_id(amenity_id)
        place.add_amenity(amenity)

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = Amenity.get_by_id(amenity_id)
        place.remove_amenity(amenity)

    def get_place_reviews(self, place_id):
        place = self.get_place(place_id)
        return place.get_reviews()

    # Méthode pour obtenir les détails complets d'un lieu, y compris le propriétaire et les aménités
    def get_place_details(self, place_id):
        place = self.get_place(place_id)
        owner = User.get_by_id(place.owner_id)
        amenities = place.get_amenities()
        reviews = place.get_reviews()
        
        place_dict = place.to_dict()
        place_dict['owner'] = owner.to_dict()
        place_dict['amenities'] = [amenity.to_dict() for amenity in amenities]
        place_dict['reviews'] = [review.to_dict() for review in reviews]
        
        return place_dict
