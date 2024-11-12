"""Review model module: Where ghosts share their haunting experiences! 👻."""

from enum import Enum
from typing import Any, Dict

from sqlalchemy.orm import relationship

from app import db
from app.models.basemodel import BaseModel
from app.utils import log_me


class ReviewRating(str, Enum):
    """The ratings a review can have! ⭐."""

    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"


class Review(BaseModel):
    """Review: A spectral critique in our haunted realm! 📝."""

    # SQLAlchemy columns
    place_id = db.Column(
        db.String(36), db.ForeignKey("place.id"), nullable=False
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("user.id"),
        nullable=True,  # Pour permettre l'anonymisation
    )
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(
        db.Enum(ReviewRating), nullable=True  # Pour permettre le soft delete
    )


    def __init__(
        self, place_id: str, user_id: str, text: str, rating: int, **kwargs
    ):
        """Initialize a new haunted review! ✨."""
        # Check if user is trying to review their own place
        try:
            from app.models.place import Place  # noqa: F811

            place = Place.get_by_id(place_id)
            if place.owner_id == user_id:
                error_msg = "Cannot review your own place"
                raise ValueError(error_msg)
        except ImportError:
            raise ValueError("Place model not implemented yet")
        except Exception as e:
            raise ValueError(str(e))
        super().__init__(**kwargs)

        # Required attributes
        self.place_id = self._validate_place_id(place_id)
        self.user_id = self._validate_user_id(user_id)
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)

    @log_me(component="business")
    def _validate_place_id(self, place_id: str) -> str:
        """Validate place ID! 🏰."""
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place ID must be a non-empty string!")

        # Vérifier que le place existe
        from app.models.place import Place  # noqa: F811

        if not Place.query.get(place_id):
            raise ValueError("Invalid place ID: place does not exist!")

        return place_id.strip()

    @log_me(component="business")
    def _validate_user_id(self, user_id: str) -> str:
        """Validate user ID! 👤."""
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string!")

        # Vérifier que l'user existe
        from app.models.user import User  # noqa: F811

        if not User.query.get(user_id):
            raise ValueError("Invalid user ID: user does not exist!")

        return user_id.strip()

    @log_me(component="business")
    def _validate_text(self, text: str) -> str:
        """Validate review text! 📝."""
        if not isinstance(text, str) or len(text.strip()) < 10:
            raise ValueError("Review text must be at least 10 characters!")
        return text.strip()

    @log_me(component="business")
    def _validate_rating(self, rating: str | None) -> ReviewRating | None:
        """Validate review rating! ⭐."""
        # Si rating est None (user soft deleted), c'est ok
        if rating is None:
            return None

        try:
            # Convertir en ReviewRating
            return ReviewRating(str(rating))
        except ValueError:
            valid_ratings = ", ".join(r.value for r in ReviewRating)
            raise ValueError(f"Rating must be one of: {valid_ratings}")

    @log_me(component="business")
    def update(self, data: dict) -> "Review":
        """Update review attributes! 📝."""
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
        except Exception as error:
            raise ValueError(f"Failed to update Review: {str(error)}")

    @log_me(component="business")
    def delete(self) -> bool:
        """Soft delete this review! 🌙."""
        try:
            return self.update(
                {
                    "rating": None,
                    "text": "[This review has been deleted]",
                    "is_deleted": True,
                }
            )
        except Exception as error:
            raise ValueError(f"Failed to soft delete Review: {str(error)}")

    @log_me(component="business")
    def anonymize(self) -> bool:
        """Anonymize review! 🎭."""
        try:
            self.user_id = None
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            raise ValueError(f"Failed to anonymize Review: {str(error)}")

    @log_me(component="business")
    def to_dict(self) -> Dict[str, Any]:
        """Transform review into dictionary! 📚."""
        base_dict = super().to_dict()
        review_dict = {
            "place_id": self.place_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating.value if self.rating else None,
            # Ajout des relations
            "place": self.place.to_dict() if self.place else None,
            "author": self.author.to_dict() if self.author else None,
        }
        return {**base_dict, **review_dict}
