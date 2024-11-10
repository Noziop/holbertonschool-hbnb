"""User model module: The ghostly users of our haunted kingdom! 👻"""

import re
from typing import TYPE_CHECKING, Any, Dict, Optional

from flask import current_app

from app import bcrypt  # Import bcrypt from app/__init__.py
from app.models.basemodel import BaseModel
from app.utils.haunted_logger import log_me

# Conditional imports for type hints
if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.review import Review


class User(BaseModel):
    """User: A spectral entity in our haunted realm! 👻"""

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        address: Optional[str] = None,
        postal_code: Optional[str] = None,
        city: Optional[str] = None,
        phone: Optional[str] = None,
        is_admin: bool = False,
        **kwargs,
    ):
        """Initialize a new spectral user! ✨"""
        # Call parent init first to set up base attributes
        super().__init__(**kwargs)

        # Then validate and set user-specific attributes
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.is_admin = is_admin

        # Hash password after validation
        self.password_hash = self._hash_password(
            self._validate_password(password)
        )

        # Optional attributes
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.phone = phone if phone else None

    @log_me(component="business")
    def _validate_username(self, username: str) -> str:
        """Validate Ghost username is conform to our spectral requirements! 👻"""
        if not isinstance(username, str) or len(username) < 3:
            raise ValueError("Username must be at least 3 characters!")
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            raise ValueError(
                "Username can only contain letters, numbers, _ and -!"
            )
        return username

    @log_me(component="business")
    def _validate_email(self, email: str) -> str:
        """Validate ghost gave as a form valid email! 📫"""
        existing = self.get_by_attr(email=email)
        if existing:
            raise ValueError("Email already in use!")
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
        ):
            raise ValueError("Invalid email format!")
        return email

    @log_me(component="business")
    def _validate_password(self, password: str) -> str:
        """Validate password : Ghosts also have standards ! 🔒"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters!")
        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter!"
            )
        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Password must contain at least one lowercase letter!"
            )
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number!")
        return password

    @log_me(component="business")
    def _validate_name(self, name: str, field: str) -> str:
        """Validate name fields! 👤"""
        if not isinstance(name, str) or len(name) < 2:
            raise ValueError(f"{field} must be at least 2 characters!")
        if not re.match(r"^[a-zA-Z\s-]+$", name):
            raise ValueError(
                f"{field} can only contain letters, spaces and -!"
            )
        return name.strip()

    @log_me(component="business")
    def _hash_password(self, password: str) -> str:
        """Hash that supernatural secret! 🔐"""
        return bcrypt.generate_password_hash(
            password, rounds=current_app.config.get("BCRYPT_LOG_ROUNDS", 12)
        ).decode("utf-8")

    @log_me(component="business")
    def check_password(self, password: str) -> bool:
        """Check if the ghost knows the secret! 🔍"""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    @log_me(component="business")
    def delete(self) -> bool:
        """Soft delete user and handle related entities! ⚰️"""
        try:
            if self.repository is None:
                raise ValueError("Repository not available")

            # 1. Hard delete des places si le modèle existe
            try:
                from app.models.place import Place

                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.hard_delete()
            except ImportError:
                pass  # Place model not implemented yet

            # 2. Anonymiser les reviews si le modèle existe
            try:
                from app.models.review import Review

                reviews = Review.get_by_attr(multiple=True, user_id=self.id)
                for review in reviews:
                    review.anonymize()
            except ImportError:
                pass  # Review model not implemented yet

            # 3. Marquer l'utilisateur comme supprimé
            self.is_active = False
            self.is_deleted = True
            self.save()

            return True

        except Exception as e:
            raise

    @log_me(component="business")
    def pause_account(self) -> bool:
        """Pause user account temporarily! 🌙"""
        try:
            # 1. Désactiver le compte
            self.is_active = False

            # 2. Cacher les places si le modèle existe
            try:
                from app.models.place import Place

                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.is_active = False
                    place.save()
            except ImportError:
                pass  # Place model not implemented yet

            self.save()
            return True

        except Exception as e:
            raise

    @log_me(component="business")
    def reactivate_account(self) -> bool:
        """Reactivate paused account! ☀️"""
        try:
            if self.is_deleted:
                raise ValueError("Cannot reactivate deleted account!")

            # 1. Réactiver le compte
            self.is_active = True

            # 2. Réactiver les places si le modèle existe
            try:
                from app.models.place import Place

                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.is_active = True
                    place.save()
            except ImportError:
                pass  # Place model not implemented yet

            self.save()
            return True

        except Exception as e:
            raise

    @log_me(component="business")
    def to_dict(self) -> Dict[str, Any]:
        """Transform user into dictionary! 📚"""
        base_dict = super().to_dict()
        user_dict = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
        }

        # Add optional attributes if they exist
        for attr in ["address", "postal_code", "city", "phone"]:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                user_dict[attr] = getattr(self, attr)

        # Never include password or hash in dict
        return {**base_dict, **user_dict}
