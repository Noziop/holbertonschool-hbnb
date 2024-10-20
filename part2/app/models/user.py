from app.persistence.repository import InMemoryRepository
from .basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import *
import re

class User(BaseModel):
    repository = InMemoryRepository()

 
    @magic_wand(validate_input(UserValidation))
    def __init__(self, username, email, password, first_name, last_name, phone_number=None, **kwargs):
        if not all([username, email, password, first_name, last_name]):
            raise ValueError("All required fields must be provided")
        
        super().__init__(**kwargs)
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password_hash = self.hash_password(self._validate_password(password))
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.phone_number = self._validate_phone_number(phone_number) if phone_number else None

    @staticmethod
    @magic_wand()
    def _validate_username(username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if len(username) < 6 or len(username) > 18:
            raise ValueError("Username must be between 6 and 18 characters long")
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        return username

    @staticmethod
    @magic_wand()
    def _validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password
    
    @staticmethod
    @magic_wand()
    def _validate_email(email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    @staticmethod
    @magic_wand()
    def _validate_name(name, field_name):
        if not isinstance(name, str):
            raise ValueError(f"{field_name} must be a string")
        if len(name) < 2 or len(name) > 50:
            raise ValueError(f"{field_name} must be between 2 and 50 characters long")
        if not re.match(r'^[a-zA-Z\s-]+$', name):
            raise ValueError(f"{field_name} can only contain letters, spaces, and hyphens")
        return name

    @staticmethod
    @magic_wand()
    def _validate_phone_number(phone_number):
        if not re.match(r'^\+?1?\d{10,14}$', phone_number):
            raise ValueError("Invalid phone number format")
        return phone_number

    @magic_wand()
    def hash_password(self, password):
        try:
            return generate_password_hash(password)
        except Exception as e:
            raise ValueError(f"Failed to hash password: {str(e)}")

    @magic_wand()
    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash is not set")
        return check_password_hash(self.password_hash, password)


    @classmethod
    @magic_wand(validate_input(UserValidation))
    def create(cls, username, email, password, first_name, last_name, phone_number=None, **kwargs):
        if cls.get_by_username(username):
            raise ValueError(f"User with username '{username}' already exists")
        if cls.get_by_email(email):
            raise ValueError(f"User with email '{email}' already exists")
        
        # Les validations de base seront effectuées par le constructeur
        user = cls(username, email, password, first_name, last_name, phone_number, **kwargs)
        cls.repository.add(user)
        return user

    @classmethod
    @magic_wand()
    def get_by_username(cls, username):
        return cls.repository.get_by_attribute('username', username)

    @classmethod
    @magic_wand()
    def get_by_email(cls, email):
        return cls.repository.get_by_attribute('email', email)

    @magic_wand(validate_input(UserValidation), update_timestamp)
    def update(self, data):
        password = data.pop('password', None)  # Retire le mot de passe du dictionnaire
        if password is not None:
            self.password_hash = self.hash_password(password)
        
        if 'username' in data and data['username'] != self.username:
            if User.get_by_username(data['username']):
                raise ValueError(f"User with username '{data['username']}' already exists")
            self.username = self._validate_username(data['username'])
        if 'email' in data and data['email'] != self.email:
            if User.get_by_email(data['email']):
                raise ValueError(f"User with email '{data['email']}' already exists")
            self.email = self._validate_email(data['email'])
        
        super().update(data)  # Appelle update de BaseModel sans le mot de passe

    @magic_wand()
    @to_dict(exclude=['password_hash'])
    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number
        })
        return user_dict
