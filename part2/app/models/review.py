"""Review Module: Because everyone's a critic, honey! 💅"""
from typing import List, Optional
from datetime import datetime, timezone
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class Review(BaseModel):
    """
    Review Model: Where we spill the tea about places! ☕

    Because if you can't say something nice...
    make sure it's at least entertaining! 💅
    """
    repository = InMemoryRepository()
    validator = ReviewValidation

    @magic_wand(validate_input(validator))
    def __init__(
        self,
        place_id: str,
        user_id: str,
        text: str,
        rating: int,
        **kwargs
    ) -> None:
        """Initialize a new Review. Time to judge! 📝"""
        super().__init__(**kwargs)
        self.place_id = self._validate_id(place_id, "place_id")
        self.user_id = self._validate_id(user_id, "user_id")
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    @staticmethod
    @magic_wand()
    def _validate_id(id_value: str, field_name: str) -> str:
        """Validate IDs. No empty tea here! 🫖"""
        if not isinstance(id_value, str):
            raise ValueError(
                f"{field_name} must be a string, darling! 💅"
            )
        if not id_value.strip():
            msg = (f"{field_name} can't be empty, "
                   "we're not that mysterious! 🕵️‍♀️")
            raise ValueError(msg)
        return id_value.strip()

    @staticmethod
    @magic_wand()
    def _validate_text(text: str) -> str:
        """Validate review text. Make it worth reading! 📚"""
        if not isinstance(text, str):
            msg = "Review must be a string, not interpretive dance! 💃"
            raise ValueError(msg)
        if len(text.strip()) < 10:
            msg = "Honey, if you can't write 10 "
            "characters, just leave 10 emojis! 🙄"
            raise ValueError(msg)
        return text.strip()

    @staticmethod
    @magic_wand()
    def _validate_rating(rating: int) -> int:
        """Validate rating. Choose your stars wisely! ⭐"""
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            msg = "Rating must be a number, not your life story! 📖"
            raise ValueError(msg)

        if not 1 <= rating <= 5:
            raise ValueError(
                "Ratings 1-5 only! This isn't your dating history! 💘"
            )
        return rating

    @classmethod
    @magic_wand(
        validate_input(validator),
        validate_entity(('Place', 'place_id'), ('User', 'user_id'))
    )
    def create(cls, place_id: str, user_id: str, text: str,
               rating: int, **kwargs) -> 'Review':
        """Create a new review. Time to spill the tea! ☕"""
        review = cls(place_id, user_id, text, rating, **kwargs)
        cls.repository.add(review)
        return review

    @classmethod
    @magic_wand(
        validate_input({'place_id': str}), 
        validate_entity('Place', 'place_id')
    )
    def get_by_place(cls, place_id: str) -> List['Review']:
        """
        Get reviews by place. As dry as the desert! 🏜️
        """
        return cls.repository.get_by_attribute('place_id', place_id, multiple=True)

    @classmethod
    @magic_wand(
        validate_input({'user_id': str}), 
        validate_entity('User', 'user_id')
    )
    def get_by_user(cls, user_id: str) -> List['Review']:
        """
        Get reviews by user. In the desert, we're all critics! 🌵
        """
        return cls.repository.get_by_attribute('user_id', user_id, multiple=True)

    @classmethod
    @magic_wand(
        validate_input({'place_id': str}), 
        validate_entity('Place', 'place_id')
    )
    def get_average_rating(cls, place_id: str) -> float:
        """
        Get average rating. Math in the desert! ✨
        """
        reviews = cls.repository.get_by_attribute('place_id', place_id, multiple=True)
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)

    @classmethod
    @magic_wand(validate_input({'limit': int}))
    def get_recent_reviews(cls, limit: int = 5) -> List['Review']:
        """Get recent reviews. Fresh tracks in the sand! 🐫"""
        all_reviews = cls.get_all()
        return sorted(
            all_reviews, 
            key=lambda x: x.created_at, 
            reverse=True
        )[:limit]

    @magic_wand(
        validate_input({'data': dict}),
        validate_entity(('Place', 'place_id'), ('User', 'user_id'))
    )
    def update(self, data: dict) -> 'Review':
        """Update review. Changed your mind? We got you! 💅"""
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            elif key == 'text':
                self.text = self._validate_text(value)
            elif key == 'rating':
                self.rating = self._validate_rating(value)
            elif key in ['place_id', 'user_id']:
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid attribute: {key}. Who are you trying to fool? 🤨"
                )

        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """Convert to dict. Serving looks in JSON format! 💃"""
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        })
        return review_dict
