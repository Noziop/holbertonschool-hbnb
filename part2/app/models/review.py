from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
# from datetime import datetime, timezone
from app.utils import *


class Review(BaseModel):
    repository = InMemoryRepository()
    validator = ReviewValidation


    @magic_wand(validate_input(validator))
    def __init__(self, place_id, user_id, text, rating, **kwargs):
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.user_id = self._validate_id(user_id, "user_id")
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    @staticmethod
    @magic_wand()
    def _validate_id(id_value, field_name):
        if not id_value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return id_value.strip()

    @staticmethod
    @magic_wand()
    def _validate_text(text):
        if len(text.strip()) < 10:
            raise ValueError("Review text must be a string with at least 10 characters")
        return text.strip()

    @staticmethod
    @magic_wand()
    def _validate_rating(rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    @classmethod
    @magic_wand(
        validate_input(validator),
        validate_entity('Place', 'place_id'), validate_entity('User', 'user_id')
    )
    def create(cls, place_id, user_id, text, rating, **kwargs):
        from .place import Place
        from .user import User
        review = cls(place_id, user_id, text, rating, **kwargs)
        cls.repository.add(review)
        logger(f"Review created: {user_id} - {review.id} - {review.text}")
        return review

    @classmethod
    @magic_wand(
        validate_input({'place_id': str}), validate_entity('Place', 'place_id')
    )
    def get_by_place(cls, place_id):
        from .place import Place
        return [review for review in cls.get_all() if review.place_id == place_id]

    @classmethod
    @magic_wand(validate_input({'user_id': str}), validate_entity('Place', 'user_id'))
    def get_by_user(cls, user_id):
        from .place import Place
        return [review for review in cls.get_all() if review.user_id == user_id]
    
    @classmethod
    @magic_wand(validate_input({'place_id': str}), validate_entity('Place', 'place_id'))
    def get_average_rating(cls, place_id):
        from .place import Place
        reviews = cls.get_by_place(place_id)
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    @classmethod
    @magic_wand(validate_input({'limit': int}))
    def get_recent_reviews(cls, limit=5):
        all_reviews = cls.get_all()
        return sorted(all_reviews, key=lambda x: x.created_at, reverse=True)[:limit]


    @magic_wand(
        validate_input({'data': dict}),
        validate_entity('Place', 'place_id'),
        validate_entity('User', 'user_id'),
        update_timestamp
    )
    def update(self, data):
        from .place import Place
        from .user import User
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue  # Skip these fields
            elif key == 'text':
                self.text = self._validate_text(value)
            elif key == 'rating':
                self.rating = self._validate_rating(value)
            elif key in ['place_id', 'user_id']:
                setattr(self, key, value)  # We've already validated these with validate_entity
            else:
                raise ValueError(f"Invalid attribute: {key}")
        super().update(data)

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        })
        return review_dict
