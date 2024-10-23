"""Base model module providing core functionality for all models."""

import uuid
import datetime as dt
from typing import Optional, Any, TypeVar, List, Union
from app.persistence.repository import InMemoryRepository
from app.utils import *


# Create a generic type for any class inheriting from BaseModel
T = TypeVar('T', bound='BaseModel')


class BaseModel:
    """
    BaseModel class providing basic CRUD operations and validation.

    Attributes:
        repository (InMemoryRepository):
        Repository instance managing data storage.

    Methods:
        __init__(**kwargs): Initialize new instance with given attributes.
        create(cls, **kwargs): Create new instance and add to repository.
        get_by_id(cls, id): Retrieve instance by ID.
        get_by_attr(cls, attr_name, value): Retrieve instance by attribute.
        get_all(cls): Retrieve all instances.
        update(self, data): Update instance with provided data.
        delete(self): Delete instance from repository.
        save(self): Save current state to repository.
        to_dict(self): Convert instance to dictionary.
    """

    repository = InMemoryRepository()

    @magic_wand(validate_input(BaseModelValidation))
    def __init__(self, **kwargs):
        """
        Initialize a new BaseModel instance.

        Args:
            **kwargs: Arbitrary keyword arguments for object attributes.

        Note:
            Creates new id, created_at and updated_at timestamps.
            Converts ISO format strings to datetime for timestamps.
        """
        self.id = str(uuid.uuid4())
        self.created_at = dt.datetime.now(dt.timezone.utc)
        self.updated_at = dt.datetime.now(dt.timezone.utc)

        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, dt.datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @classmethod
    @magic_wand(validate_input({'id': str}))
    def get_by_id(cls: type[T], id: str) -> T:
        """
        Retrieve an object by its unique identifier.

        Args:
            id (str): The unique identifier of the object.

        Returns:
            T: The instance matching the ID.

        Raises:
            ValueError: If no object is found with this ID.
        """
        obj = cls.repository.get(id)
        if obj is None:
            raise ValueError(f"No {cls.__name__} found with id: {id}")
        return obj

    @classmethod
    @magic_wand()
    def get_by_attr(
        cls: type[T],
        multiple: bool = False,
        **kwargs: Any
    ) -> Union[Optional[T], List[T]]:
        """
        Summon entities by their attributes! 👻
        
        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: Your supernatural search criteria! 🔮
        """
        return cls.repository.get_by_attribute(multiple=multiple, **kwargs)

    @classmethod
    @magic_wand()
    def get_all(cls: type[T]) -> List[T]:
        """
        Retrieve all objects of this type.

        Returns:
            List[T]: List of all instances.

        Note:
            Returns empty list if no objects exist.
        """
        return cls.repository.get_all()

    @classmethod
    @magic_wand(validate_input({'**kwargs': dict}))
    def create(cls: type[T], **kwargs) -> T:
        """
        Create and store a new instance.

        Args:
            **kwargs: Attributes to initialize the instance.

        Returns:
            T: The newly created instance.
        """
        instance = cls(**kwargs)
        cls.repository.add(instance)
        return instance

    @magic_wand(validate_input({'data': dict}))
    def update(self, data: dict) -> T:
        """
        Update the instance with new data.

        Args:
            data (dict): Dictionary of attributes to update.

        Returns:
            T: The updated instance.

        Raises:
            ValueError: If updating protected attributes or invalid attribute.
        """
        for key, value in data.items():
            if key in ['id', 'created_at']:
                raise ValueError(f"Cannot update {key} attribute")
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self.save()
        return self

    @magic_wand(validate_entity('BaseModel', 'id'))
    def delete(self) -> bool:
        """
        Delete the instance from storage.

        Returns:
            bool: True if deletion was successful.

        Raises:
            ValueError: If instance not found in storage.
        """
        if not self.repository.get(self.id):
            raise ValueError(
                f"No {self.__class__.__name__} found with id: {self.id}"
            )
        self.repository.delete(self.id)
        return True

    @magic_wand(validate_input({'data': dict}), update_timestamp)
    def save(self) -> T:
        """
        Save the instance to storage.

        Returns:
            T: The saved instance.

        Raises:
            ValueError: If save operation fails.
        """
        try:
            data = self.to_dict()
            data.pop('id', None)
            data.pop('created_at', None)
            self.repository.update(self.id, data)
            return self
        except Exception as e:
            raise ValueError(f"Failed to save: {str(e)}")

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self) -> dict:
        """
        Convert instance to dictionary.

        Returns:
            dict: Dictionary containing instance attributes.

        Note:
            Converts datetime objects to ISO format strings.
        """
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
