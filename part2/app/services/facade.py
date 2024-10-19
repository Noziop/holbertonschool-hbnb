from app.models.user import User
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity

class HBnBFacade:
    def __init__(self):
        self.user_repository = User.repository
        self.place_repository = Place.repository
        self.amenity_repository = Amenity.repository
        self.review_repository = Review.repository
        self.placemaneity_repository = PlaceAmenity.repository

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
        try:
            user = User.get_by_username(username)
            if not user:
                raise ValueError(f"No user found with username: {username}")
            return user
        except ValueError as e:
            raise ValueError(f"Failed to get user by username: {str(e)}")

    def get_user_by_email(self, email):
        try:
            user = User.get_by_email(email)
            if not user:
                raise ValueError(f"No user found with email: {email}")
            return user
        except ValueError as e:
            raise ValueError(f"Failed to get user by email: {str(e)}")

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
            if not user:
                raise ValueError(f"No user found with id: {user_id}")
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
        try:
            return Place.get_all()
        except ValueError as e:
            raise ValueError(f"Failed to get all places: {str(e)}")

    def get_places_by_city(self, city):
        try:
            Place.get_by_city(city)
        except ValueError as e:
            raise ValueError(f"Failed to get places by city: {str(e)}")

    def get_places_by_country(self, country):
        try:
            Place.get_by_country(country)
        except ValueError as e:
            raise ValueError(f"Failed to get places by country: {str(e)}")

    def get_places_by_price_range(self, min_price, max_price):
        try:
            Place.get_by_price_range(min_price, max_price)
        except ValueError as e:
            raise ValueError(f"Failed to get places by price range: {str(e)}")

    def get_places_by_capacity(self, min_guests):
        try:
            Place.get_by_capacity(min_guests)
        except ValueError as e:
            raise ValueError(f"Failed to get places by capacity: {str(e)}")

    def get_places_by_location(self, latitude, longitude, radius):
        try:
            Place.get_by_location(latitude, longitude, radius)
        except ValueError as e:
            raise ValueError(f"Failed to get places by location: {str(e)}")

    def search_places(self, keywords):
        try:
            Place.search(keywords)
        except ValueError as e:
            raise ValueError(f"Failed to search places: {str(e)}")

    def get_place_amenities(self, place_id):
        try :
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            return place.get_amenities()
        except ValueError as e:
            raise ValueError(f"Failed to get place amenities: {str(e)}")

    def add_amenity_to_place(self, place_id, amenity_id):
        try:
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            amenity = Amenity.get_by_id(amenity_id)
            if not amenity:
                raise ValueError(f"No amenity found with id: {amenity_id}")
            place.add_amenity(amenity)
        except ValueError as e:
            raise ValueError(f"Failed to add amenity to place: {str(e)}")

    def remove_amenity_from_place(self, place_id, amenity_id):
        try:
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            amenity = Amenity.get_by_id(amenity_id)
            if not amenity:
                raise ValueError(f"No amenity found with id: {amenity_id}")
            place.remove_amenity(amenity)
        except ValueError as e:
            raise ValueError(f"Failed to remove amenity from place: {str(e)}")
        
    def get_place_reviews(self, place_id):
        try:
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            return place.get_reviews()
        except ValueError as e:
            raise ValueError(f"Failed to get place reviews: {str(e)}")

    # Méthode pour obtenir les détails complets d'un lieu, y compris le propriétaire et les aménités
    def get_place_details(self, place_id):
        try:
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"No place found with id: {place_id}")
            owner = User.get_by_id(place.owner_id)
            if not owner:
                raise ValueError(f"No owner found for place with id: {place_id}")
            amenities = place.get_amenities()
            if not amenities:
                raise ValueError(f"No amenities found for place with id: {place_id}")
            reviews = place.get_reviews()
            if not reviews:
                raise ValueError(f"No reviews found for place with id: {place_id}")
            
            place_dict = place.to_dict()
            place_dict['owner'] = owner.to_dict()
            place_dict['amenities'] = [amenity.to_dict() for amenity in amenities]
            place_dict['reviews'] = [review.to_dict() for review in reviews]
            
            return place_dict
        except ValueError as e:
            raise ValueError(f"Failed to get place details: {str(e)}")

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
        try:
            return Review.get_all()
        except ValueError as e:
            raise ValueError(f"Failed to get all reviews: {str(e)}")

    def get_reviews_by_place(self, place_id):
        try:
            return Review.get_by_place(place_id)
        except ValueError as e:
            raise ValueError(f"Failed to get reviews by place: {str(e)}")

    def get_reviews_by_user(self, user_id):
        try:
            return Review.get_by_user(user_id)
        except ValueError as e:
            raise ValueError(f"Failed to get reviews by user: {str(e)}")

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
        try:
            all_reviews = self.get_all_reviews()
            if not all_reviews:
                raise ValueError("No reviews found")
            return sorted(all_reviews, key=lambda x: x.created_at, reverse=True)[:limit]
        except ValueError as e:
            raise ValueError(f"Failed to get recent reviews: {str(e)}")
    
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
        try:
            return Amenity.get_all()
        except ValueError as e:
            raise ValueError(f"Failed to get all amenities: {str(e)}")

    def get_amenities_by_name(self, name):
        try:
            return Amenity.get_by_name(name)
        except ValueError as e:
            raise ValueError(f"Failed to get amenities by name: {str(e)}")

    def search_amenities(self, keyword):
        try:
            return Amenity.search(keyword)
        except ValueError as e:
            raise ValueError(f"Failed to search amenities: {str(e)}")

    # Méthode pour obtenir les lieux associés à une aménité
    def get_places_with_amenity(self, amenity_id):
        from app.models.placeamenity import PlaceAmenity
        from app.models.place import Place
        try:
            place_amenities = PlaceAmenity.get_by_amenity(amenity_id)
            if not place_amenities:
                raise ValueError(f"No places found with amenity id: {amenity_id}")
            return [Place.get_by_id(pa.place_id) for pa in place_amenities]
        except ValueError as e:
            raise ValueError(f"Failed to get places with amenity: {str(e)}")

    # PlaceAmenity methods
    def create_place_amenity(self, place_id, amenity_id):
        try:
            # Vérifier si le place_id et le amenity_id existent
            place = Place.get_by_id(place_id) or Place.get_by_name(place_id)
            if not place:
                raise ValueError(f"No place found with id or name: {place_id}")
            
            amenity = Amenity.get_by_id(amenity_id) or Amenity.get_by_name(amenity_id)
            if not amenity:
                raise ValueError(f"No amenity found with id or name: {amenity_id}")
            
            place_amenity = PlaceAmenity.create(place_id=place.id, amenity_id=amenity.id)
            return place_amenity
        except ValueError as e:
            raise ValueError(f"Failed to create {place.name}'s {amenity.name}: {str(e)}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {str(e)}")


    def get_place_amenities(self, place_id):
        try:
            return PlaceAmenity.get_by_place(place_id)
        except ValueError as e:
            raise ValueError(f"Failed to get {place_id} amenities: {str(e)}")

    def get_amenity_places(self, amenity_id):
        try:
            return PlaceAmenity.get_by_amenity(amenity_id)
        except ValueError as e:
            raise ValueError(f"Failed to get {amenity_id} places: {str(e)}")

    def get_places_with_amenity(self, amenity_id):
        try:
            return PlaceAmenity.get_places(amenity_id)
        except ValueError as e:
            raise ValueError(f"Failed to get places with {amenity_id}: {str(e)}")

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
    def get_amenities_for_place(self, place_id):
        try:
            place = self.get_place(place_id)  # This will raise ValueError if place doesn't exist
            place_amenities = self.get_place_amenities(place_id)
            return [Amenity.get_by_id(pa.amenity_id) for pa in place_amenities]
        except ValueError as e:
            raise ValueError(f"Failed to get amenities for {place}: {str(e)}")
        
    # Méthode pour ajouter un aménité à un lieu
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
    def remove_amenity_from_place(self, place_id, amenity_id):
        try
            self.delete_place_amenity(place_id, amenity_id)
        except ValueError as e: 
            raise ValueError(f"Failed to remove amenity from place: {str(e)}")
