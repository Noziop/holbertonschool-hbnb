from app.models.user import User
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repository = User.repository
        self.place_repository = Place.repository
        self.amenity_repository = Amenity.repository
        self.review_repository = Review.repository
        self.placemaneity_repository = PlaceAmenity.repository
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

    # Review methods
    def create_review(self, review_data):
        try:
            # Vérifier si le place_id et le user_id existent
            Place.get_by_id(review_data['place_id'])
            User.get_by_id(review_data['user_id'])
            return Review.create(**review_data)
        except ValueError as e:
            raise ValueError(f"Failed to create review: {str(e)}")

    def get_review(self, review_id):
        try:
            return Review.get_by_id(review_id)
        except ValueError as e:
            raise ValueError(f"Failed to get review: {str(e)}")

    def update_review(self, review_id, review_data):
        try:
            review = self.get_review(review_id)
            review.update(review_data)
            return review
        except ValueError as e:
            raise ValueError(f"Failed to update review: {str(e)}")

    def get_all_reviews(self):
        return Review.get_all()

    def get_reviews_by_place(self, place_id):
        return Review.get_by_place(place_id)

    def get_reviews_by_user(self, user_id):
        return Review.get_by_user(user_id)

    def delete_review(self, review_id):
        try:
            review = self.get_review(review_id)
            review.delete()
        except ValueError as e:
            raise ValueError(f"Failed to delete review: {str(e)}")

    # Méthode pour obtenir la note moyenne d'un lieu
    def get_place_average_rating(self, place_id):
        reviews = self.get_reviews_by_place(place_id)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    # Méthode pour obtenir les avis les plus récents
    def get_recent_reviews(self, limit=5):
        all_reviews = self.get_all_reviews()
        return sorted(all_reviews, key=lambda x: x.created_at, reverse=True)[:limit]
    
    # Amenity methods
    def create_amenity(self, amenity_data):
        try:
            return Amenity.create(**amenity_data)
        except ValueError as e:
            raise ValueError(f"Failed to create amenity: {str(e)}")

    def get_amenity(self, amenity_id):
        try:
            return Amenity.get_by_id(amenity_id)
        except ValueError as e:
            raise ValueError(f"Failed to get amenity: {str(e)}")

    def update_amenity(self, amenity_id, amenity_data):
        try:
            amenity = self.get_amenity(amenity_id)
            amenity.update(amenity_data)
            return amenity
        except ValueError as e:
            raise ValueError(f"Failed to update amenity: {str(e)}")

    def get_all_amenities(self):
        return Amenity.get_all()

    def get_amenities_by_name(self, name):
        return Amenity.get_by_name(name)

    def search_amenities(self, keyword):
        return Amenity.search(keyword)

    # Méthode pour obtenir les lieux associés à une aménité
    def get_places_with_amenity(self, amenity_id):
        from app.models.placeamenity import PlaceAmenity
        from app.models.place import Place
        place_amenities = PlaceAmenity.get_by_amenity(amenity_id)
        return [Place.get_by_id(pa.place_id) for pa in place_amenities]

    # PlaceAmenity methods
    def create_place_amenity(self, place_id, amenity_id):
        try:
            # Vérifier si le place_id et le amenity_id existent
            Place.get_by_id(place_id)
            Amenity.get_by_id(amenity_id)
            return PlaceAmenity.create(place_id=place_id, amenity_id=amenity_id)
        except ValueError as e:
            raise ValueError(f"Failed to create place amenity: {str(e)}")

    def get_place_amenities(self, place_id):
        return PlaceAmenity.get_by_place(place_id)

    def get_amenity_places(self, amenity_id):
        return PlaceAmenity.get_by_amenity(amenity_id)

    def get_places_with_amenity(self, amenity_id):
        return PlaceAmenity.get_places(amenity_id)

    def delete_place_amenity(self, place_id, amenity_id):
        place_amenities = PlaceAmenity.get_by_place(place_id)
        for pa in place_amenities:
            if pa.amenity_id == amenity_id:
                pa.delete()
                return
        raise ValueError(f"No PlaceAmenity found for place_id {place_id} and amenity_id {amenity_id}")

    # Méthode pour obtenir tous les aménités d'un lieu
    def get_amenities_for_place(self, place_id):
        place = self.get_place(place_id)  # This will raise ValueError if place doesn't exist
        place_amenities = self.get_place_amenities(place_id)
        return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]

    # Méthode pour ajouter un aménité à un lieu
    def add_amenity_to_place(self, place_id, amenity_id):
        place_amenities = PlaceAmenity.get_by_place(place_id)
        for pa in place_amenities:
            if pa.amenity_id == amenity_id:
                return pa  # L'association existe déjà, on la retourne
        return self.create_place_amenity(place_id, amenity_id)

    # Méthode pour retirer un aménité d'un lieu
    def remove_amenity_from_place(self, place_id, amenity_id):
        self.delete_place_amenity(place_id, amenity_id)
