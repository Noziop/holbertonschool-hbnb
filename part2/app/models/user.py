# app/models/user.py
"""User model module: The ghostly users of our haunted kingdom! 👻"""
from typing import Optional, Dict, Any, TYPE_CHECKING
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app.models.basemodel import BaseModel

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
        **kwargs
    ):
        """Initialize a new spectral user! ✨"""
        self.logger.debug(f"Creating new User with username: {username}")
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
        self.logger.debug(f"Validating username: {username}")
        if not isinstance(username, str) or len(username) < 3:
            error_msg = "Username must be at least 3 characters!"
            self.logger.error(f"Username validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            error_msg = "Username can only contain letters, numbers, _ and -!"
            self.logger.error(f"Username validation failed: {error_msg}")
            raise ValueError(error_msg)
        return username

    def _validate_email(self, email: str) -> str:
        """Validate email! 📫"""
        self.logger.debug(f"Validating email: {email}")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            error_msg = "Invalid email format!"
            self.logger.error(f"Email validation failed: {error_msg}")
            raise ValueError(error_msg)
        return email

    def _validate_password(self, password: str) -> str:
        """Validate password! 🔒"""
        self.logger.debug("Validating password")
        if len(password) < 8:
            error_msg = "Password must be at least 8 characters!"
            self.logger.error(f"Password validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.search(r'[A-Z]', password):
            error_msg = "Password must contain at least one uppercase letter!"
            self.logger.error(f"Password validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.search(r'[a-z]', password):
            error_msg = "Password must contain at least one lowercase letter!"
            self.logger.error(f"Password validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.search(r'\d', password):
            error_msg = "Password must contain at least one number!"
            self.logger.error(f"Password validation failed: {error_msg}")
            raise ValueError(error_msg)
        return password

    def _validate_name(self, name: str, field: str) -> str:
        """Validate name fields! 👤"""
        self.logger.debug(f"Validating {field}: {name}")
        if not isinstance(name, str) or len(name) < 2:
            error_msg = f"{field} must be at least 2 characters!"
            self.logger.error(f"Name validation failed: {error_msg}")
            raise ValueError(error_msg)
        if not re.match(r'^[a-zA-Z\s-]+$', name):
            error_msg = f"{field} can only contain letters, spaces and -!"
            self.logger.error(f"Name validation failed: {error_msg}")
            raise ValueError(error_msg)
        return name.strip()

    def _hash_password(self, password: str) -> str:
        """Hash the password! 🔐"""
        self.logger.debug("Hashing password")
        return generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches! 🔍"""
        self.logger.debug("Checking password")
        return check_password_hash(self.password_hash, password)

    def delete(self) -> bool:
        """Soft delete user and handle related entities! ⚰️"""
        try:
            self.logger.debug(f"Attempting to soft delete user: {self.username}")
            
            # 1. Hard delete des places si le modèle existe
            try:
                from app.models.place import Place
                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.hard_delete()
                    self.logger.info(f"Hard deleted place: {place.id}")
            except ImportError:
                self.logger.warning("Place model not implemented yet")
            
            # 2. Anonymiser les reviews si le modèle existe
            try:
                from app.models.review import Review
                reviews = Review.get_by_attr(multiple=True, user_id=self.id)
                for review in reviews:
                    review.anonymize()
                    self.logger.info(f"Anonymized review: {review.id}")
            except ImportError:
                self.logger.warning("Review model not implemented yet")
            
            # 3. Marquer l'utilisateur comme supprimé
            self.is_active = False
            self.is_deleted = True
            self.save()
            
            self.logger.info(f"Successfully soft deleted user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete user {self.username}: {str(e)}")
            raise

    def pause_account(self) -> bool:
        """Pause user account temporarily! 🌙"""
        try:
            self.logger.debug(f"Attempting to pause account for user: {self.username}")
            
            # 1. Désactiver le compte
            self.is_active = False
            
            # 2. Cacher les places si le modèle existe
            try:
                from app.models.place import Place
                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.is_active = False
                    place.save()
                    self.logger.info(f"Deactivated place: {place.id}")
            except ImportError:
                self.logger.warning("Place model not implemented yet")
            
            self.save()
            self.logger.info(f"Successfully paused account for user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to pause account for user {self.username}: {str(e)}")
            raise

    def reactivate_account(self) -> bool:
        """Reactivate paused account! ☀️"""
        try:
            self.logger.debug(f"Attempting to reactivate account for user: {self.username}")
            
            if self.is_deleted:
                error_msg = "Cannot reactivate deleted account!"
                self.logger.error(f"{error_msg} User: {self.username}")
                raise ValueError(error_msg)
            
            # 1. Réactiver le compte
            self.is_active = True
            
            # 2. Réactiver les places si le modèle existe
            try:
                from app.models.place import Place
                places = Place.get_by_attr(multiple=True, owner_id=self.id)
                for place in places:
                    place.is_active = True
                    place.save()
                    self.logger.info(f"Reactivated place: {place.id}")
            except ImportError:
                self.logger.warning("Place model not implemented yet")
            
            self.save()
            self.logger.info(f"Successfully reactivated account for user: {self.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reactivate account for user {self.username}: {str(e)}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """Transform user into dictionary! 📚"""
        self.logger.debug(f"Converting user {self.username} to dictionary")
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