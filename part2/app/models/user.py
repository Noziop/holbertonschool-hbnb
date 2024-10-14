from app.persistence.repository import InMemoryRepository
from app.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, username, email, password, first_name=None, last_name=None, phone_number=None, **kwargs):
        super().__init__(**kwargs)
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password_hash = self.hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = self._validate_phone_number(phone_number) if phone_number else None

    @classmethod
    def create(cls, username, email, password, **kwargs):
        if cls.get_by_username(username):
            raise ValueError(f"User with username '{username}' already exists")
        if cls.get_by_email(email):
            raise ValueError(f"User with email '{email}' already exists")
        
        user = cls(username, email, password, **kwargs)
        cls.repository.add(user)
        return user

    @classmethod
    def get_by_username(cls, username):
        return cls.repository.get_by_attribute('username', username)

    @classmethod
    def get_by_email(cls, email):
        return cls.repository.get_by_attribute('email', email)


    def update(self, data):
        password = data.pop('password', None)  # Retire le mot de passe du dictionnaire
        if password is not None:
            self.password_hash = self.hash_password(password)
        
        if 'username' in data:
            self.username = self._validate_username(data['username'])
        if 'email' in data:
            self.email = self._validate_email(data['email'])
        
        super().update(data)  # Appelle update de BaseModel sans le mot de passe

    def _validate_username(self, username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if len(username) < 6 or len(username) > 18:
            raise ValueError("Username must be between 6 and 18 characters long")
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        return username

    def _validate_email(self, email):
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        # Expression régulière pour vérifier le format de base de l'email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        
        return email

    def hash_password(self, password):
        try:
            return generate_password_hash(password)
        except Exception as e:
            raise ValueError(f"Failed to hash password: {str(e)}")

    def check_password(self, password):
        if not self.password_hash:
            raise ValueError("Password hash is not set")
        return check_password_hash(self.password_hash, password)
    
    def _validate_phone_number(self, phone_number):
        if not re.match(r'^\+?1?\d{10,14}$', phone_number):
            raise ValueError("Invalid phone number format")
        return phone_number

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