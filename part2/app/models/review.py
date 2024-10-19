from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from datetime import datetime, timezone
from app.utils.magic_wands import log_action, error_handler, validate_input, update_timestamp, to_dict_decorator, validate_entity_exists
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    repository = InMemoryRepository()

    @log_action
    @error_handler
    @validate_input(place_id=str, user_id=str, text=str, rating=int)
    def __init__(self, place_id, user_id, text, rating, **kwargs):
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.user_id = self._validate_id(user_id, "user_id")
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    @staticmethod
    @log_action
    @error_handler
    def _validate_id(id_value, field_name):
        if not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @staticmethod
    @log_action
    @error_handler
    def _validate_text(text):
        if len(text.strip()) < 10:
            raise ValueError("Review text must be a string with at least 10 characters")
        return text.strip()

    @staticmethod
    @log_action
    @error_handler
    def _validate_rating(rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @classmethod
    @log_action
    @error_handler
    @validate_input(place_id=str, user_id=str, text=str, rating=int)
    @validate_entity_exists(lambda place_id, *args: Place.get_by_id(place_id))
    @validate_entity_exists(lambda place_id, user_id, *args: User.get_by_id(user_id))
    def create(cls, place_id, user_id, text, rating, **kwargs):
        review = cls(place_id, user_id, text, rating, **kwargs)
        cls.repository.add(review)
        return review

    @classmethod
    @log_action
    @error_handler
    @validate_input(place_id=str)
    @validate_entity_exists(lambda place_id: Place.get_by_id(place_id))
    def get_by_place(cls, place_id):
        return [review for review in cls.get_all() if review.place_id == place_id]

    @classmethod
    @log_action
    @error_handler
    @validate_input(user_id=str)
    @validate_entity_exists(lambda user_id: User.get_by_id(user_id))
    def get_by_user(cls, user_id):
        return [review for review in cls.get_all() if review.user_id == user_id]
    
    @classmethod
    @log_action
    @error_handler
    @validate_input(place_id=str)
    @validate_entity_exists(lambda place_id: Place.get_by_id(place_id))
    def get_average_rating(cls, place_id):
        reviews = cls.get_by_place(place_id)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @classmethod
    @log_action
    @error_handler
    @validate_input(limit=int)
    def get_recent_reviews(cls, limit=5):
        all_reviews = cls.get_all()
        return sorted(all_reviews, key=lambda x: x.created_at, reverse=True)[:limit]

    @log_action
    @error_handler
    @update_timestamp
    @validate_input(data=dict)
    def update(self, data):
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at', 'place_id', 'user_id']:
                continue  # Skip these fields
            elif key == 'text':
                self.text = self._validate_text(value)
            elif key == 'rating':
                self.rating = self._validate_rating(value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

    @to_dict_decorator()
    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        })
        return review_dict
