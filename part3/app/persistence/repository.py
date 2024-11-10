"""Repository pattern for our haunted database! 👻."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Union, TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.utils import log_me

if TYPE_CHECKING:
    from app.models.basemodel import BaseModel

    ModelType = TypeVar("ModelType", bound="BaseModel")
else:
    ModelType = TypeVar("ModelType", bound=db.Model)


class Repository(ABC):
    """Abstract base class for all our haunted repositories! 👻."""

    @abstractmethod
    def add(self, obj: ModelType) -> ModelType:
        """Add a new spirit to our realm."""
        pass

    @abstractmethod
    def get(self, obj_id: str) -> Optional[ModelType]:
        """Summon a specific spirit."""
        pass

    @abstractmethod
    def get_all(self) -> List[ModelType]:
        """Summon all spirits."""
        pass

    @abstractmethod
    def update(self, obj_id: str, data: dict) -> Optional[ModelType]:
        """Update a spirit's essence."""
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        """Banish a spirit."""
        pass

    @abstractmethod
    def get_by_attribute(
        self, multiple: bool = False, **kwargs: Any
    ) -> Union[Optional[ModelType], List[ModelType]]:
        """
        Get objects by attributes.

        Summoning entities from the storage beyond! 👻.

        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: The dark specifications (each more cursed than the last!)
        """
        pass


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of our haunted repository! 👻."""

    def __init__(self, model: type[ModelType]):
        """Initialize with a specific model class."""
        self.model = model

    @log_me(component="persistence")
    def add(self, obj: ModelType) -> ModelType:
        """Add a new spirit to our realm."""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as error:
            db.session.rollback()
            raise ValueError(f"Failed to add: {str(error)}")

    @log_me(component="persistence")
    def get(self, obj_id: str) -> Optional[ModelType]:
        """Summon a specific spirit."""
        return self.model.query.get(obj_id)

    @log_me(component="persistence")
    def get_all(self) -> List[ModelType]:
        """Summon all spirits."""
        return self.model.query.filter_by(is_deleted=False).all()

    @log_me(component="persistence")
    def update(self, obj_id: str, data: dict) -> Optional[ModelType]:
        """Update a spirit's essence."""
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
            return obj
        except SQLAlchemyError as error:
            db.session.rollback()
            raise ValueError(f"Failed to update: {str(error)}")

    @log_me(component="persistence")
    def delete(self, obj_id: str) -> bool:
        """Banish a spirit."""
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as error:
            db.session.rollback()
            raise ValueError(f"Failed to delete: {str(error)}")

    @log_me(component="persistence")
    def get_by_attribute(
        self, multiple: bool = False, **kwargs: Any
    ) -> Union[Optional[ModelType], List[ModelType]]:
        """
        Get objects by attributes.

        Summoning entities from the storage beyond! 👻.

        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: The dark specifications (each more cursed than the last!)
        """
        query = self.model.query.filter_by(**kwargs, is_deleted=False)
        return query.all() if multiple else query.first()
