from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class Review(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, place_id, user_id, text, rating):
        super().__init__()
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
        except ValueError:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @classmethod
    def create(cls, place_id, user_id, text, rating):
        review = cls(place_id, user_id, text, rating)
        cls.repository.add(review)
        return review

    @classmethod
    def get_by_id(cls, review_id):
        return cls.repository.get(review_id)

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    @classmethod
    def get_by_place(cls, place_id):
        return [review for review in cls.get_all() if review.place_id == place_id]

    @classmethod
    def get_by_user(cls, user_id):
        return [review for review in cls.get_all() if review.user_id == user_id]

    def update(self, data):
        if 'text' in data:
            self.text = self._validate_text(data['text'])
        if 'rating' in data:
            self.rating = self._validate_rating(data['rating'])
        self.repository.update(self.id, self)

    def delete(self):
        self.repository.delete(self.id)

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        })
        return review_dict