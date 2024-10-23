"""
User Module: Because basic authentication is so 2010! 💅

This module defines the User class with all its fabulous features:
- Secure password handling (no 'password123' allowed, honey! 🙄)
- Email validation (we're not savages! ✨)
- Phone number formatting (because standards matter! 📱)
"""

from typing import Optional, List
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import re
from .basemodel import BaseModel
from app.persistence.repository import InMemoryRepository
from app.utils import *


class User(BaseModel):
    """
    User Model: For those who are too fabulous for basic CRUD! ✨

    Attributes:
        repository: Where we keep all our precious users
        username: Your digital identity (make it werk! 💃)
        email: How we slide into your inbox 📧
        password_hash: Your secrets are safe with us 🔐
        first_name: What your mama calls you
        last_name: What your mama shouts when you're in trouble
        phone_number: For those "u up?" moments 📱
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
        **kwargs
    ) -> None:
        """
        Initialize a new User. Welcome to the party! 🎉

        Args:
            username: Your digital alter ego
            email: Your @ identity
            password: Your secret handshake
            first_name: The name on your Starbucks cup
            last_name: The name on your credit card
            phone_number: For those who still make calls (how retro! 📞)
        """
        if not all([username, email, password, first_name, last_name]):
            msg = "All required fields must be provided, darling! 💋"
            raise ValueError(msg)
        
        super().__init__(**kwargs)
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password_hash = self.hash_password(
            self._validate_password(password)
        )
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.phone_number = (
            self._validate_phone_number(phone_number) 
            if phone_number else None
        )

        # === VALIDATION METHODS === #
    @staticmethod
    @magic_wand()
    def _validate_username(username: str) -> str:
        """Validate that username. Make it werk! 💃"""
        if not isinstance(username, str):
            raise ValueError("Username must be a string, duh! 🙄")
        if len(username) < 6 or len(username) > 18:
            raise ValueError(
                "Username length 6-18 chars. We have standards! 💅"
            )
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValueError(
                "Letters, numbers, underscores, hyphens only. Keep it classy! ✨"
            )
        return username

    @staticmethod
    @magic_wand()
    def _validate_password(password: str) -> str:
        """
        Validate password. Because 'password123' is SO 2010! 🙄
        """
        if len(password) < 8:
            raise ValueError("Password too short. That's what she said! 😏")
        if not re.search(r"\d", password):
            raise ValueError("Add a number. Because reasons! 🔢")
        if not re.search(r"[A-Z]", password):
            raise ValueError("CAPS LOCK IS NOT JUST FOR YELLING! 🗣️")
        if not re.search(r"[a-z]", password):
            raise ValueError("lowercase is love, lowercase is life 💕")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Add some spice! (special characters) 🌶️")
        return password

    @staticmethod
    @magic_wand(validate_input({'email': str}))
    def _validate_email(email: str) -> str:
        """Validate email. No fake addresses from your ex! 📧"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError(
                "Invalid email format. Who are you trying to fool? 🕵️‍♀️"
            )
        return email

    @staticmethod
    @magic_wand()
    def _validate_name(name: str, field_name: str) -> str:
        """Validate names. No 'xX_D4rk_L0rd_Xx' allowed! 🙄"""
        if not isinstance(name, str):
            raise ValueError(f"{field_name} must be a string, honey! 💁‍♀️")
        if len(name) < 2 or len(name) > 50:
            raise ValueError(
                f"{field_name} length 2-50 chars. We're not writing a novel! 📚"
            )
        if not re.match(r'^[a-zA-Z\s-]+$', name):
            raise ValueError(
                f"{field_name}: letters, spaces, hyphens only. Keep it real! ✨"
            )
        return name

    @staticmethod
    @magic_wand()
    def _validate_phone_number(phone: str) -> str:
        """Validate phone number. For booty calls only! 📱"""
        if not re.match(r'^\+?1?\d{10,14}$', phone):
            raise ValueError(
                "Invalid phone format. Who are you trying to ghost? 👻"
            )
        return phone
    
        # === GET/SEARCH METHODS === #
    @classmethod
    @magic_wand()
    def search(cls, **criteria) -> List['User']:
        """
        Search users. Stalking made professional! 🕵️‍♀️
        """
        if not criteria:
            return cls.get_all()  # Show me EVERYBODY! 

        results = cls.get_all()
        for attr, value in criteria.items():
            if value is not None:
                results = [
                    user for user in results
                    if getattr(user, attr, None) == value
                ]
        return results

    # === PASSWORD HANDLING === #
    @magic_wand()
    def hash_password(self, password: str) -> str:
        """
        Hash that password! Making your secrets extra spicy! 🌶️
        """
        try:
            return generate_password_hash(password)
        except Exception as e:
            raise ValueError(
                f"Hash failed. Even the algorithm can't handle this! 💅 {str(e)}"
            )

    @magic_wand()
    def check_password(self, password: str) -> bool:
        """
        Check password. No sneaking into DMs! 🔐
        """
        if not self.password_hash:
            raise ValueError("No password set. How mysterious! 🧐")
        return check_password_hash(self.password_hash, password)

    # === CREATE/UPDATE METHODS === #
    @classmethod
    @magic_wand(validate_input(UserValidation))
    def create(cls, **kwargs) -> 'User':
        """
        Create new user. Fresh meat! 🥩... I mean, welcome! 🎉
        """
        username = kwargs.get('username')
        email = kwargs.get('email')
        
        if cls.get_by_attr('username', username):
            raise ValueError(
                f"Username '{username}' is taken. Be more creative! 💭"
            )
        if cls.get_by_attr('email', email):
            raise ValueError(
                f"Email '{email}' exists. Nice try! 😏"
            )
        
        user = cls(**kwargs)
        cls.repository.add(user)
        return user

    @magic_wand(validate_input(UserValidation))
    def update(self, data: dict) -> 'User':
        """
        Update user. New phone, who dis? 📱
        """
        password = data.pop('password', None)
        if password:
            self.password_hash = self.hash_password(password)
        
        if 'username' in data and data['username'] != self.username:
            if User.get_by_attr('username', data['username']):
                raise ValueError("Username taken! Snooze you lose! 😴")
        if 'email' in data and data['email'] != self.email:
            if User.get_by_attr('email', data['email']):
                raise ValueError("Email exists! Double life much? 🕵️‍♀️")
        
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at', 'password_hash']:
                continue
            
            if hasattr(self, f'_validate_{key}'):
                value = getattr(self, f'_validate_{key}')(value)
            elif not hasattr(self, key):
                raise ValueError(
                    f"Invalid attribute: {key}. Who you trying to fool? 🤨"
                )
                
            setattr(self, key, value)
        
        self.updated_at = datetime.now(timezone.utc)
        self.repository._storage[self.id] = self
        return self

    # === SERIALIZATION === #
    @magic_wand()
    @to_dict(exclude=['password_hash'])
    def to_dict(self) -> dict:
        """
        Convert to dict. Spilling the tea, but keeping the secrets! ☕
        """
        base_dict = super().to_dict()
        user_dict = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number
        }
        return {**base_dict, **user_dict}