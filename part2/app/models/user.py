# app/models/user.py
"""User model module: The ghostly users of our haunted kingdom! 👻"""
from typing import Optional, Dict, Any, TYPE_CHECKING, List
from werkzeug.security import generate_password_hash, check_password_hash
import re
import logging
from app.models.basemodel import BaseModel

# Conditionally import Place and Review for type hints and avoid circular imports
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
        **kwargs
    ):
        """Initialize a new spectral user! ✨"""
        super().__init__(**kwargs)
        
        # Validate and set required attributes
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password_hash = self._hash_password(self._validate_password(password))
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.is_admin = is_admin
        
        # Optional attributes
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.phone = phone if phone else None
        
        self.logger.info(f"Created new User with username: {self.username}")

    def _validate_username(self, username: str) -> str:
        """Validate username! 👻"""
        if not isinstance(username, str) or len(username) < 3:
            raise ValueError("Username must be at least 3 characters! 👻")
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, _ and -! 🧙‍♀️")
        return username

    def _validate_email(self, email: str) -> str:
        """Validate email! 📫"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format! 📧")
        return email

    def _validate_password(self, password: str) -> str:
        """Validate password! 🔒"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters! 🔑")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter! 🔒")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter! 🔑")
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number! 🔢")
        return password

    def _validate_name(self, name: str, field: str) -> str:
        """Validate name fields! 👤"""
        if not isinstance(name, str) or len(name) < 2:
            raise ValueError(f"{field} must be at least 2 characters! 👻")
        if not re.match(r'^[a-zA-Z\s-]+$', name):
            raise ValueError(f"{field} can only contain letters, spaces and -! 🧙‍♀️")
        return name.strip()

    def _hash_password(self, password: str) -> str:
        """Hash the password! 🔐"""
        return generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches! 🔍"""
        return check_password_hash(self.password_hash, password)

    def hard_delete(self) -> bool:
        """Hard delete user and all related entities! ⚰️"""
        try:
            # 1. Hard delete des places (et leurs reviews associées)
            places = Place.get_by_attr(multiple=True, owner_id=self.id)
            for place in places:
                place.hard_delete()
                self.logger.info(f"Hard deleted place: {place.id}")
            
            # 2. Hard delete des reviews de l'utilisateur
            reviews = Review.get_by_attr(multiple=True, user_id=self.id)
            for review in reviews:
                review.hard_delete()
                self.logger.info(f"Hard deleted review: {review.id}")
            
            # 3. Hard delete de l'utilisateur
            super().hard_delete()
            self.logger.info(f"Hard deleted user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to hard delete user: {str(e)}")
            raise

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
                self.logger.warning("Place model not implemented yet")
            
            self.save()
            self.logger.info(f"Account paused for user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to pause account: {str(e)}")
            raise

    def reactivate_account(self) -> bool:
        """Reactivate paused account! ☀️"""
        try:
            if self.is_deleted:
                raise ValueError("Cannot reactivate deleted account! 👻")
            
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
                self.logger.warning("Place model not implemented yet")
            
            self.save()
            self.logger.info(f"Account reactivated for user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reactivate account: {str(e)}")
            raise

    def delete(self) -> bool:
        """Soft delete user and handle related entities! ⚰️"""
        try:
            # 1. Hard delete des places si le modèle existe
            try:
                from app.models.place import Place
                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.hard_delete()
            except ImportError:
                self.logger.warning("Place model not implemented yet")
            
            # 2. Anonymiser les reviews si le modèle existe
            try:
                from app.models.review import Review
                reviews = Review.get_by_attr(multiple=True, user_id=self.id)
                for review in reviews:
                    review.anonymize()
            except ImportError:
                self.logger.warning("Review model not implemented yet")
            
            # 3. Marquer l'utilisateur comme supprimé
            self.is_active = False
            self.is_deleted = True
            self.save()
            
            self.logger.info(f"Soft deleted user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete user: {str(e)}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """Transform user into dictionary! 📚"""
        base_dict = super().to_dict()
        user_dict = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin
        }
        
        # Add optional attributes if they exist
        for attr in ['address', 'postal_code', 'city', 'phone']:
            if hasattr(self, attr) and getattr(self, attr) is not None:
                user_dict[attr] = getattr(self, attr)
        
        # Never include password or hash in dict
        return {**base_dict, **user_dict}