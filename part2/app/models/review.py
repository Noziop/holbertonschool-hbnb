# app/models/review.py
"""Review model module: Where ghosts share their haunting experiences! 👻"""
import re
from typing import TYPE_CHECKING, Any, Dict, Optional

from app.models.basemodel import BaseModel

# Conditional imports for type hints
if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.user import User


class Review(BaseModel):
    """Review: A spectral critique in our haunted realm! 📝"""

    def __init__(self, place_id: str, user_id: str, text: str, rating: int, **kwargs):
        """Initialize a new haunted review! ✨"""
        self.logger.debug(f"Creating new Review for place: {place_id}")

        # Check if user is trying to review their own place
        try:
            from app.models.place import Place

            place = Place.get_by_id(place_id)
            if place.owner_id == user_id:
                error_msg = "Cannot review your own place"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
        except ImportError:
            self.logger.warning("Place model not implemented yet")

        self.logger.debug(f"Creating new Review for place: {place_id}")
        super().__init__(**kwargs)

        # Required attributes
        self.place_id = self._validate_place_id(place_id)
        self.user_id = self._validate_user_id(user_id)
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

        self.logger.info(f"Created new Review with ID: {self.id}")

    def _validate_place_id(self, place_id: str) -> str:
        """Validate place ID! 🏰"""
        self.logger.debug(f"Validating place ID: {place_id}")
        if not isinstance(place_id, str) or not place_id.strip():
            error_msg = "Place ID must be a non-empty string!"
            self.logger.error(f"Place ID validation failed: {error_msg}")
            raise ValueError(error_msg)
        return place_id.strip()

    def _validate_user_id(self, user_id: str) -> str:
        """Validate user ID! 👤"""
        self.logger.debug(f"Validating user ID: {user_id}")
        if not isinstance(user_id, str) or not user_id.strip():
            error_msg = "User ID must be a non-empty string!"
            self.logger.error(f"User ID validation failed: {error_msg}")
            raise ValueError(error_msg)
        return user_id.strip()

    def _validate_text(self, text: str) -> str:
        """Validate review text! 📝"""
        self.logger.debug("Validating review text")
        if not isinstance(text, str) or len(text.strip()) < 10:
            error_msg = "Review text must be at least 10 characters!"
            self.logger.error(f"Text validation failed: {error_msg}")
            raise ValueError(error_msg)
        return text.strip()

    def _validate_rating(self, rating: int | None) -> int | None:
        """Validate review rating! ⭐"""
        self.logger.debug(f"Validating rating: {rating}")

        # Si rating est None (user soft deleted), c'est ok
        if rating is None:
            return None

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                error_msg = "Rating must be between 1 and 5!"
                self.logger.error(f"Rating validation failed: {error_msg}")
                raise ValueError(error_msg)
            return rating
        except (TypeError, ValueError) as e:
            self.logger.error(f"Rating validation failed: {str(e)}")
            raise ValueError("Rating must be a number between 1 and 5!")

    def update(self, data: dict) -> "Review":
        """Update review attributes! 📝"""
        self.logger.debug(f"Attempting to update Review: {self.id}")
        try:
            # Validate new values before update
            if "text" in data:
                data["text"] = self._validate_text(data["text"])
            if "rating" in data:
                data["rating"] = self._validate_rating(data["rating"])
            if "place_id" in data:
                data["place_id"] = self._validate_place_id(data["place_id"])
            if "user_id" in data:
                data["user_id"] = self._validate_user_id(data["user_id"])

            return super().update(data)
        except Exception as e:
            self.logger.error(f"Failed to update Review: {str(e)}")
            raise

    # app/models/review.py
    def delete(self) -> bool:
        """Soft delete this review! 🌙"""
        try:
            self.logger.debug(f"Soft deleting Review: {self.id}")
            return self.update(
                {"rating": None, "text": "[This user has deleted his account]"}
            )
        except Exception as e:
            self.logger.error(f"Failed to soft delete Review: {str(e)}")
            raise

    def anonymize(self) -> None:
        """Anonymize review! 🎭"""
        self.logger.debug(f"Anonymizing Review: {self.id}")
        self.user_id = None
        self.save()
        self.logger.info(f"Successfully anonymized Review: {self.id}")

    def to_dict(self) -> Dict[str, Any]:
        """Transform review into dictionary! 📚"""
        self.logger.debug(f"Converting review {self.id} to dictionary")
        base_dict = super().to_dict()
        review_dict = {
            "place_id": self.place_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating,
        }
        return {**base_dict, **review_dict}
