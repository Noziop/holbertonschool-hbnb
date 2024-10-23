"""Base model module: The dark foundation of our haunted kingdom! 👻"""

import uuid
import datetime as dt
from typing import Optional, Any, TypeVar, List, Union
from app.persistence.repository import InMemoryRepository
from app.utils import *

# Create a generic type for our supernatural entities
T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """
    BaseModel: The supernatural ancestor of all our haunted models! 🏰
    
    Like a ghost whisperer for data, it provides the dark arts of:
    - CRUD operations (Create, Raise from dead, Update curses, Delete souls)
    - Validation (Even spirits need standards!)
    - Storage management (Our ethereal database)
    
    Think of it as the Haunted Mansion's foundation - spooky but reliable! 🏚️
    """
    repository = InMemoryRepository()

    @magic_wand(validate_input(BaseModelValidation))
    def __init__(self, **kwargs):
        """
        Summon a new instance from the void! ✨
        
        Args:
            **kwargs: The mystical ingredients for our creation ritual 🔮
        
        Note:
            Creates a unique soul (id) and timestamps its birth in our realm!
        """
        self.id = str(uuid.uuid4())  # Every spirit needs a unique identifier!
        self.created_at = dt.datetime.now(dt.timezone.utc)  # Time of summoning
        self.updated_at = dt.datetime.now(dt.timezone.utc)  # Last haunting

        # Bind the ethereal attributes
        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, dt.datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @classmethod
    @magic_wand(validate_input({'id': str}))
    def get_by_id(cls: type[T], id: str) -> T:
        """
        Find a spirit by their ethereal ID! 👻
        
        Args:
            id: The supernatural identifier
        
        Raises:
            ValueError: When the spirit has vanished into thin air! 👻
        """
        obj = cls.repository.get(id)
        if obj is None:
            raise ValueError(f"No {cls.__name__} found! The spirit has moved on! 👻")
        return obj

    @classmethod
    @magic_wand()
    def get_by_attr(cls: type[T], multiple: bool = False, **kwargs: Any) -> Union[Optional[T], List[T]]:
        """
        Search the spirit realm by attributes! 🔮
        
        Args:
            multiple: Summon one spirit or the whole haunted house? 
            **kwargs: The supernatural search criteria
        """
        return cls.repository.get_by_attribute(multiple=multiple, **kwargs)

    @classmethod
    @magic_wand()
    def get_all(cls: type[T]) -> List[T]:
        """Summon ALL the spirits! A supernatural roll call! 👻"""
        return cls.repository.get_all()

    @classmethod
    @magic_wand(validate_input({'**kwargs': dict}))
    def create(cls: type[T], **kwargs) -> T:
        """
        Bring a new entity into our haunted realm! 🌙
        
        Args:
            **kwargs: The dark ingredients for our creation
        """
        instance = cls(**kwargs)
        cls.repository.add(instance)
        return instance

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> T:
        """
        Update a spirit's attributes! Like a supernatural makeover! ✨
        
        Raises:
            ValueError: When the dark magic fails! 
        """
        for key, value in data.items():
            if key in ['id', 'created_at']:
                raise ValueError(f"Cannot alter the {key}! Some curses are permanent! 🔮")
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}! What kind of dark magic is this? 🧙‍♀️")
        self.save()
        return self

    @magic_wand(validate_entity('BaseModel', 'id'))
    def delete(self) -> bool:
        """Banish this entity back to the void! ⚰️"""
        if not self.repository.get(self.id):
            raise ValueError(f"Cannot banish what's already gone! 👻")
        self.repository.delete(self.id)
        return True

    @magic_wand(validate_input({'data': dict}), update_timestamp)
    def save(self) -> T:
        """
        Preserve this spirit in our ethereal storage! 📜
        
        Raises:
            ValueError: When the preservation spell fails! 
        """
        try:
            data = self.to_dict()
            data.pop('id', None)  # Some attributes are sacred
            data.pop('created_at', None)  # Birth time is immutable
            self.repository.update(self.id, data)
            return self
        except Exception as e:
            raise ValueError(f"The preservation spell failed: {str(e)} 🔮")

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """Transform this supernatural entity into mortal-readable format! 📚"""
        return {
            'id': self.id,
            'created_at': (
                self.created_at.isoformat()
                if isinstance(self.created_at, dt.datetime)
                else self.created_at
            ),
            'updated_at': (
                self.updated_at.isoformat()
                if isinstance(self.updated_at, dt.datetime)
                else self.updated_at
            )
        }