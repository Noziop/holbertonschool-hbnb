from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class Review(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, place_id, user_id, text, rating, **kwargs):
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.user_id = self._validate_id(user_id, "user_id")
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    @staticmethod
    def _validate_id(id_value, field_name):
        if not isinstance(id_value, str) or not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @staticmethod
    def _validate_text(text):
        if not isinstance(text, str) or len(text.strip()) < 10:
            raise ValueError("Review text must be a string with at least 10 characters")
        return text.strip()

    @staticmethod
    def _validate_rating(rating):
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @classmethod
    def create(cls, place_id, user_id, text, rating, **kwargs):
        try:
            review = cls(place_id, user_id, text, rating, **kwargs)
            cls.repository.add(review)
            return review
        except ValueError as e:
            raise ValueError(f"Failed to create review: {str(e)}")

    @classmethod
    def get_by_place(cls, place_id):
        return [review for review in cls.get_all() if review.place_id == place_id]

    @classmethod
    def get_by_user(cls, user_id):
        return [review for review in cls.get_all() if review.user_id == user_id]

    def update(self, data):
        try:
            if 'place_id' in data:
                self.place_id = self._validate_id(data['place_id'], "place_id")
            if 'user_id' in data:
                self.user_id = self._validate_id(data['user_id'], "user_id")
            if 'text' in data:
                self.text = self._validate_text(data['text'])
            if 'rating' in data:
                self.rating = self._validate_rating(data['rating'])
            
            # Retirer les attributs spécifiques à Review avant d'appeler super().update()
            for attr in ['place_id', 'user_id', 'text', 'rating']:
                data.pop(attr, None)
            
            super().update(data)
        except ValueError as e:
            raise ValueError(f"Failed to update review: {str(e)}")

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        })
        return review_dict