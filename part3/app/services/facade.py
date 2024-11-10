# app/services/facade.py
"""The haunted gateway to our supernatural kingdom! 👻"""

import logging
from typing import Any, Dict, List, Optional, Type, TypeVar

from app.models.amenity import Amenity
from app.models.basemodel import BaseModel
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity
from app.models.review import Review
from app.models.user import User

# Créer un type générique pour nos modèles
T = TypeVar("T", bound=BaseModel)


class HBnBFacade:
    """The haunted gateway to our supernatural kingdom! 👻"""

    def __init__(self):
        """Summon our mystical repositories! 🔮"""
        self.logger = logging.getLogger("hbnb_models")
        self.logger.info("HBnB Facade initialized! ✨")

    def create(self, model_class: Type[T], data: dict) -> T:
        """Create a new haunted entity! ✨"""
        try:
            self.logger.debug(f"Creating {model_class.__name__} with data: {data}")
            instance = model_class(**data)
            instance.save()
            self.logger.info(f"Created {model_class.__name__} with ID: {instance.id}")
            return instance
        except Exception as e:
            self.logger.error(f"Failed to create {model_class.__name__}: {str(e)}")
            raise

    def get(self, model_class: Type[T], id: str) -> T:
        """Find an entity by its spectral ID! 🔍"""
        try:
            self.logger.debug(f"Getting {model_class.__name__} with ID: {id}")
            instance = model_class.get_by_id(id)
            self.logger.info(f"Found {model_class.__name__} with ID: {id}")
            return instance
        except Exception as e:
            self.logger.error(f"Failed to get {model_class.__name__}: {str(e)}")
            raise

    def update(self, model_class: Type[T], id: str, data: dict) -> T:
        """Update a haunted entity! 🌟"""
        try:
            self.logger.debug(f"Updating {model_class.__name__} {id} with data: {data}")
            instance = self.get(model_class, id)
            updated = instance.update(data)
            self.logger.info(f"Updated {model_class.__name__} with ID: {id}")
            return updated
        except Exception as e:
            self.logger.error(f"Failed to update {model_class.__name__}: {str(e)}")
            raise

    def delete(self, model_class: Type[T], id: str, hard: bool = False) -> bool:
        """Banish an entity from our realm! ⚡"""
        try:
            self.logger.debug(
                f"{'Hard' if hard else 'Soft'} deleting {model_class.__name__} with ID: {id}"
            )
            instance = self.get(model_class, id)

            if hard:
                result = instance.hard_delete()
                self.logger.info(f"Hard deleted {model_class.__name__} with ID: {id}")
            else:
                result = instance.delete()
                self.logger.info(f"Soft deleted {model_class.__name__} with ID: {id}")

            return result
        except Exception as e:
            self.logger.error(f"Failed to delete {model_class.__name__}: {str(e)}")
            raise

    def find(self, model_class: Type[T], **criteria) -> List[T]:
        """Search for entities in our realm! 🔮"""
        try:
            self.logger.debug(
                f"Finding {model_class.__name__} with criteria: {criteria}"
            )
            instances = model_class.get_by_attr(multiple=True, **criteria)
            self.logger.info(f"Found {len(instances)} {model_class.__name__}(s)")
            return instances
        except Exception as e:
            self.logger.error(f"Failed to find {model_class.__name__}: {str(e)}")
            raise

    # Méthode spéciale pour PlaceAmenity
    def link_place_amenity(self, place_id: str, amenity_id: str) -> PlaceAmenity:
        """Create a haunted link between place and amenity! 🔗"""
        try:
            self.logger.debug(f"Linking place {place_id} with amenity {amenity_id}")
            link = PlaceAmenity(place_id=place_id, amenity_id=amenity_id)
            link.save()
            self.logger.info(
                f"Created link between place {place_id} and amenity {amenity_id}"
            )
            return link
        except Exception as e:
            self.logger.error(f"Failed to create place-amenity link: {str(e)}")
            raise
