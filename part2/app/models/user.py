from werkzeug.security import generate_password_hash, check_password_hash
import re
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from typing import Optional, List
from app.utils import *


class User(BaseModel):
    """
    User Model: The mortals who dare to haunt our places! 👻
    
    Each user is a potential spirit in our haunted marketplace,
    seeking their perfect haunting grounds! 🏚️
    """
    repository = InMemoryRepository()

    @magic_wand(validate_input(UserValidation))
    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        postal_code: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        **kwargs
    ) -> None:
        """Summon a new user into existence! 👻"""
        super().__init__(**kwargs)
        
        # Required soul bindings
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password_hash = self.hash_password(self._validate_password(password))
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        
        # Optional enchantments
        self.phone_number = self._validate_phone_number(phone_number) if phone_number else None
        self.address = self._validate_address(address) if address else None
        self.postal_code = self._validate_postal_code(postal_code) if postal_code else None
        self.city = self._validate_city(city) if city else None
        self.country = self._validate_country(country) if country else None

    # === VALIDATION METHODS === #
    @staticmethod
    @magic_wand()
    def _validate_address(address: str) -> str:
        """Validate mortal's dwelling location! 🏚️"""
        if not isinstance(address, str) or len(address.strip()) < 5:
            raise ValueError("Address must be a proper location, not a ghost address! 👻")
        return address.strip()

    @staticmethod
    @magic_wand()
    def _validate_postal_code(postal_code: str) -> str:
        """Validate postal code for our supernatural mail service! 📬"""
        if not re.match(r'^\d{4,10}$', postal_code):
            raise ValueError("Postal code must be 4-10 digits! Even ghosts need proper mail! 📮")
        return postal_code

    @staticmethod
    @magic_wand()
    def _validate_city(city: str) -> str:
        """Validate city of haunting! 🌃"""
        if not re.match(r'^[a-zA-Z\s-]{2,50}$', city):
            raise ValueError("City must be a real place, not a supernatural realm! 🌙")
        return city.strip()

    @staticmethod
    @magic_wand()
    def _validate_country(country: str) -> str:
        """Validate country of residence! 🌍"""
        if not re.match(r'^[a-zA-Z\s-]{2,50}$', country):
            raise ValueError("Country must exist in the mortal realm! 🗺️")
        return country.strip()

    @staticmethod
    @magic_wand()
    def _validate_username(username: str) -> str:
        """Validate username like a ghost checking IDs at a haunted club! 👻"""
        if not isinstance(username, str):
            raise ValueError("Username must be a string, mortal! 🧟‍♀️")
        if len(username) < 6 or len(username) > 18:
            raise ValueError(
                "Username must be 6-18 chars. Like a proper spell incantation! 🔮"
            )
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            msg = ("Only letters, numbers, underscores, and hyphens - "
                "This isn't a supernatural summoning! 🧙‍♀️")
            raise ValueError(msg)
        return username

    @staticmethod
    @magic_wand()
    def _validate_password(password: str) -> str:
        """
        Validate password like checking the secret knock at a haunted house! 🏚️
        """
        if len(password) < 8:
            raise ValueError("Password too short! Even ghosts have standards! 👻")
        if not re.search(r"\d", password):
            raise ValueError("Add a number! Count like a vampire counts victims! 🧛‍♀️")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Add capitals! Like a ghost's dramatic entrance! 👻")
        if not re.search(r"[a-z]", password):
            raise ValueError("Add lowercase! Like whispers in a haunted hall! 🏰")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Add special chars! Like cursed symbols! ⚰️")
        return password

    @staticmethod
    @magic_wand(validate_input({'email': str}))
    def _validate_email(email: str) -> str:
        """Validate email like checking ghost mail addresses! 📫"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError(
                "Invalid email format! Even spirits need proper addresses! 👻"
            )
        return email

    @staticmethod
    @magic_wand()
    def _validate_name(name: str, field_name: str) -> str:
        """Validate names like checking tombstone engravings! 🪦"""
        if not isinstance(name, str):
            raise ValueError(f"{field_name} must be a string, spirit! 👻")
        if len(name) < 2 or len(name) > 50:
            raise ValueError(
                f"{field_name} must be 2-50 chars. Like a proper epitaph! ⚰️"
            )
        if not re.match(r'^[a-zA-Z\s-]+$', name):
            raise ValueError(
                f"{field_name}: letters, spaces, hyphens only. This isn't a curse! 🧙‍♀️"
            )
        return name

    @staticmethod
    @magic_wand()
    def _validate_phone_number(phone: str) -> str:
        """Validate phone number like a supernatural hotline! ☎️"""
        if not re.match(r'^\+?1?\d{10,14}$', phone):
            raise ValueError(
                "Invalid phone format! How will the spirits reach you? 👻"
            )
        return phone

        # === GET/SEARCH METHODS === #
    @classmethod
    @magic_wand()
    def search(cls, **criteria) -> List['User']:
        """
        Search for lost souls in our database! 👻
        Like a supernatural detective agency, but more organized!
        """
        if not criteria:
            return cls.get_all()  # Summon ALL the spirits! 🌙
        
        return cls.get_by_attr(multiple=True, **criteria)

    # === PASSWORD HANDLING === #
    @magic_wand()
    def hash_password(self, password: str) -> str:
        """
        Hash that password like sealing a cursed tomb! 🔮
        Not even the most powerful spirits can break this seal!
        """
        try:
            return generate_password_hash(password)
        except Exception as e:
            msg = (f"The dark magic failed! Even our strongest "
                f"encryption spells couldn't handle this! ⚡ {str(e)}")
            raise ValueError(msg)

    @magic_wand()
    def check_password(self, password: str) -> bool:
        """
        Check password like a supernatural bouncer! 🧟‍♀️
        No entry without the proper incantation!
        """
        if not self.password_hash:
            raise ValueError("No password set! Even ghosts need security! 👻")
        return check_password_hash(self.password_hash, password)

    # === CREATE/UPDATE METHODS === #
    @classmethod
    @magic_wand(validate_input(UserValidation))
    def create(cls, **kwargs) -> 'User':
        """
        Summon a new user into existence! 🧙‍♀️
        Like creating a new ghost, but with better documentation!
        """
        username = kwargs.get('username')
        email = kwargs.get('email')
        
        # Check if the spirit name is taken
        if cls.get_by_attr(username=username):
            raise ValueError(
                f"The name '{username}' is already haunting our database! 👻"
            )
        
        # Check if the spectral email exists
        if cls.get_by_attr(email=email):
            raise ValueError(
                f"This email '{email}' already belongs to another spirit! 📧"
            )
        
        return super().create(**kwargs)

    @magic_wand(validate_input(UserValidation))
    def update(self, data: dict) -> 'User':
        """
        Update user like renovating a haunted mansion! 🏚️
        Every ghost needs a makeover sometimes!
        """
        # Handle the secret incantation (password)
        password = data.pop('password', None)
        if password:
            self.password_hash = self.hash_password(password)

        # Check for spirit name conflicts
        if 'username' in data and data['username'] != self.username:
            if User.get_by_attr(username=data['username']):
                raise ValueError("This spirit name is already haunting us! 👻")
        
        # Check for spectral email duplicates
        if 'email' in data and data['email'] != self.email:
            if User.get_by_attr(email=data['email']):
                raise ValueError("This ethereal email is already in use! 📫")

        # Update the haunted attributes
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at', 'password_hash']:
                continue  # Some things are sacred, even for ghosts! 

            if hasattr(self, f'_validate_{key}'):
                value = getattr(self, f'_validate_{key}')(value)
            elif not hasattr(self, key):
                raise ValueError(
                    f"Invalid attribute: {key}. What kind of dark magic is this? 🔮"
                )

            setattr(self, key, value)

        # Mark the time of transformation
        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    # === SERIALIZATION === #
    @magic_wand()
    @to_dict(exclude=['password_hash'])
    def to_dict(self) -> dict:
        """
        Transform this spirit into mortal-readable format! 📜
        Revealing all secrets... except the password, of course! 🤫
        """
        base_dict = super().to_dict()
        user_dict = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': getattr(self, 'address', None),
            'postal_code': getattr(self, 'postal_code', None),
            'city': getattr(self, 'city', None),
            'country': getattr(self, 'country', None)
        }
        return {**base_dict, **user_dict}
