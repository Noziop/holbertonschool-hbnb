# app/models/basemodel.py
"""Base model module: The dark foundation of our haunted kingdom! 👻"""
import uuid
import datetime as dt
import logging
from typing import Optional, Any, TypeVar, List, Union
from app.persistence.repository import InMemoryRepository

# Create a generic type for our supernatural entities
T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """BaseModel: The supernatural ancestor of all our haunted models! 🏰"""
    repository = InMemoryRepository()
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Summon a new instance from the void! ✨"""
        self.id = str(uuid.uuid4())
        self.created_at = dt.datetime.now(dt.timezone.utc)
        self.updated_at = dt.datetime.now(dt.timezone.utc)
        self.is_active = True      # Visibility / pause
        self.is_deleted = False    # soft delete

        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, dt.datetime.fromisoformat(value))
            else:
                setattr(self, key, value)
        
        self.logger.info(f"Created new {self.__class__.__name__} with ID: {self.id}")

    def save(self) -> T:
        """Preserve this spirit in our ethereal storage! 📜"""
        try:
            self.repository.add(self)
            self.logger.info(f"Saved {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            self.logger.error(f"Failed to save {self.__class__.__name__}: {str(e)}")
            raise ValueError(f"The preservation spell failed: {str(e)} 🔮")

    def update(self, data: dict) -> T:
        """Update a spirit's attributes! ✨"""
        try:
            # Vérifier les attributs protégés
            protected = {'id', 'created_at', 'is_deleted'}
            if any(attr in data for attr in protected):
                raise ValueError("Cannot alter sacred attributes! 🔮")
            
            # Mettre à jour ou ajouter les attributs
            for key, value in data.items():
                setattr(self, key, value)
            
            # Mettre à jour le timestamp
            self.updated_at = dt.datetime.now(dt.timezone.utc)
            self.save()
            self.logger.info(f"Updated {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            self.logger.error(f"Failed to update {self.__class__.__name__}: {str(e)}")
            raise ValueError(f"The update spell failed: {str(e)} 🔮")

    def hard_delete(self) -> bool:
        """Actually delete from repository! ⚰️"""
        try:
            if not self.repository.get(self.id):
                raise ValueError("Cannot banish what's already gone! 👻")
            self.repository.delete(self.id)
            self.logger.info(f"Hard deleted {self.__class__.__name__} with ID: {self.id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to hard delete {self.__class__.__name__}: {str(e)}")
            raise

    @classmethod
    def get_by_id(cls: type[T], id: str) -> T:
        """Find a spirit by their ethereal ID! 👻"""
        obj = cls.repository.get(id)
        if obj is None:
            cls.logger.warning(f"No {cls.__name__} found with ID: {id}")
            raise ValueError(f"No {cls.__name__} found! The spirit has moved on! 👻")
        return obj

    @classmethod
    def get_by_attr(cls: type[T], multiple: bool = False, **kwargs: Any) -> Union[Optional[T], List[T]]:
        """Search the spirit realm by attributes! 🔮"""
        return cls.repository.get_by_attribute(multiple=multiple, **kwargs)

    def to_dict(self) -> dict:
        """Transform this supernatural entity into mortal-readable format! 📚"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'is_deleted': self.is_deleted
        }

    def __str__(self) -> str:
        """Return a haunted string representation! 📝"""
        return (
            f'<{self.__class__.__name__} '
            f'id={self.id} '
            f'created_at={self.created_at.isoformat()} '
            f'updated_at={self.updated_at.isoformat()} '
            f'is_active={self.is_active} '
            f'is_deleted={self.is_deleted}>'
        )

    def __repr__(self) -> str:
        return self.__str__()# app/models/basemodel.py
"""Base model module: The dark foundation of our haunted kingdom! 👻"""
import uuid
import datetime as dt
import logging
from typing import Optional, Any, TypeVar, List, Union
from app.persistence.repository import InMemoryRepository

# Create a generic type for our supernatural entities
T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """BaseModel: The supernatural ancestor of all our haunted models! 🏰"""
    repository = InMemoryRepository()
    logger = logging.getLogger('hbnb_models')

    def __init__(self, **kwargs):
        """Initialize a new haunted instance! ✨"""
        self.id = str(uuid.uuid4())
        self.created_at = dt.datetime.now(dt.timezone.utc)
        self.updated_at = dt.datetime.now(dt.timezone.utc)
        self.is_active = True      # For visibility/pause state
        self.is_deleted = False    # For soft delete state

        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, dt.datetime.fromisoformat(value))
            else:
                setattr(self, key, value)
        
        self.logger.debug(f"Creating new {self.__class__.__name__}")
        self.logger.info(f"Created {self.__class__.__name__} with ID: {self.id}")

    def save(self) -> T:
        """Save instance to repository! 📜"""
        try:
            self.logger.debug(f"Attempting to save {self.__class__.__name__} with ID: {self.id}")
            self.repository.add(self)
            self.logger.info(f"Successfully saved {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            self.logger.error(f"Failed to save {self.__class__.__name__}: {str(e)}")
            raise ValueError(f"Save operation failed: {str(e)} 🔮")

    def update(self, data: dict) -> T:
        """Update instance attributes! ✨"""
        try:
            self.logger.debug(f"Attempting to update {self.__class__.__name__} with ID: {self.id}")
            
            # Check protected attributes
            protected = {'id', 'created_at', 'is_deleted'}
            if any(attr in data for attr in protected):
                error_msg = f"Cannot modify protected attributes: {protected & data.keys()}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Update attributes
            for key, value in data.items():
                setattr(self, key, value)
            
            # Update timestamp
            self.updated_at = dt.datetime.now(dt.timezone.utc)
            self.save()
            
            self.logger.info(f"Successfully updated {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            self.logger.error(f"Update failed for {self.__class__.__name__}: {str(e)}")
            raise ValueError(f"Update operation failed: {str(e)} 🔮")

    def hard_delete(self) -> bool:
        """Permanently delete instance from repository! ⚰️"""
        try:
            self.logger.debug(f"Attempting hard delete of {self.__class__.__name__} with ID: {self.id}")
            
            if not self.repository.get(self.id):
                error_msg = f"Entity not found: {self.id}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
                
            self.repository.delete(self.id)
            self.logger.info(f"Successfully deleted {self.__class__.__name__} with ID: {self.id}")
            return True
        except Exception as e:
            self.logger.error(f"Hard delete failed for {self.__class__.__name__}: {str(e)}")
            raise

    @classmethod
    def get_by_id(cls: type[T], id: str) -> T:
        """Retrieve instance by ID! 👻"""
        cls.logger.debug(f"Attempting to retrieve {cls.__name__} with ID: {id}")
        obj = cls.repository.get(id)
        if obj is None:
            error_msg = f"Entity not found: {id}"
            cls.logger.warning(error_msg)
            raise ValueError(error_msg)
        cls.logger.info(f"Successfully retrieved {cls.__name__} with ID: {id}")
        return obj

    @classmethod
    def get_by_attr(cls: type[T], multiple: bool = False, **kwargs: Any) -> Union[Optional[T], List[T]]:
        """Search instances by attributes! 🔮"""
        cls.logger.debug(f"Searching {cls.__name__} with attributes: {kwargs}")
        result = cls.repository.get_by_attribute(multiple=multiple, **kwargs)
        if result:
            cls.logger.info(f"Found {len(result) if multiple else 1} {cls.__name__}(s)")
        else:
            cls.logger.info(f"No {cls.__name__} found matching criteria")
        return result

    def to_dict(self) -> dict:
        """Convert instance to dictionary! 📚"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'is_deleted': self.is_deleted
        }

    def __str__(self) -> str:
        """String representation of instance! 📝"""
        return (
            f'<{self.__class__.__name__} '
            f'id={self.id} '
            f'created_at={self.created_at.isoformat()} '
            f'updated_at={self.updated_at.isoformat()} '
            f'is_active={self.is_active} '
            f'is_deleted={self.is_deleted}>'
        )

    def __repr__(self) -> str:
        return self.__str__()