"""The haunted gateway to our supernatural kingdom! 👻"""

from typing import List, Type, TypeVar, Union

from app.models import *  # On importe tous nos modèles d'un coup !
from app.models.basemodel import BaseModel
from app.utils import log_me

# Créer un type générique pour nos modèles
T = TypeVar("T", bound=BaseModel)


class HBnBFacade:
    """The haunted gateway to our supernatural kingdom! 👻"""

    @log_me(component="business")
    def login(self, email: str, password: str) -> User:
        """Authenticate a ghost in our realm! 👻"""
        if not email or not password:
            raise ValueError("Email and password are required! 👻")

        # On utilise la méthode spécifique du modèle User
        user = User.authenticate(email, password)
        if not user:
            raise ValueError("This spirit is not registered in our realm! 👻")
        if not user.is_active:
            raise ValueError("This spirit has been exorcised! 👻")

        return user

    @log_me(component="business")
    def create(self, model_class: Type[T], data: dict) -> T:
        """Create a new haunted entity! ✨"""
        if not data:
            raise ValueError("No data provided for creation")
        if not issubclass(model_class, BaseModel):
            raise ValueError("Invalid model class")

        try:
            instance = model_class(**data)
            return instance.save()
        except Exception as e:
            raise ValueError(f"Failed to create: {str(e)}")

    @log_me(component="business")
    def get(self, model_class: Type[T], id: str) -> T:
        """Find an entity by its spectral ID! 🔍"""
        if not id:
            raise ValueError("No ID provided")
        if not issubclass(model_class, BaseModel):
            raise ValueError("Invalid model class")

        instance = model_class.get_by_id(id)
        if not instance:
            raise ValueError(f"{model_class.__name__} not found with ID: {id}")
        return instance

    @log_me(component="business")
    def update(
        self,
        model_class: Type[T],
        id: str,
        data: dict,
        user_id: str = None,
        is_admin: bool = False,
    ) -> T:
        """Update a haunted entity! 🌟"""
        if not data:
            raise ValueError("No data provided for update")
        if not issubclass(model_class, BaseModel):
            raise ValueError("Invalid model class")

        instance = self.get(model_class, id)

        # Vérifier les permissions
        if not instance.can_be_managed_by(user_id, is_admin):
            raise ValueError("You cannot modify this resource! 👻")

        return instance.update(data)

    @log_me(component="business")
    def delete(
        self,
        model_class: Type[T],
        id: str,
        user_id: str = None,
        is_admin: bool = False,
        hard: bool = False,
    ) -> bool:
        """Banish an entity from our realm! ⚡"""
        if not issubclass(model_class, BaseModel):
            raise ValueError("Invalid model class")

        instance = self.get(model_class, id)  # Vérifie déjà l'existence

        # Vérifier les permissions
        if not instance.can_be_managed_by(user_id, is_admin):
            raise ValueError("You cannot delete this resource! 👻")

        return instance.hard_delete() if hard else instance.delete()

    @log_me(component="business")
    def find(self, model_class: Type[T], **criteria) -> List[T]:
        """Search for entities in our realm! 🔮"""
        if not issubclass(model_class, BaseModel):
            raise ValueError("Invalid model class")

        # Si pas de critères, on retourne tout
        if not criteria:
            # Debug print
            return model_class.get_all()

        # Sinon on cherche avec les critères
        return model_class.find_by(multiple=True, **criteria)

    @log_me(component="business")
    def link_place_amenity(
        self,
        place_id: str,
        amenity_id: str,
        user_id: str = None,
        is_admin: bool = False,
    ) -> PlaceAmenity:
        """Create a haunted link between place and amenity! 🔗"""
        if not place_id or not amenity_id:
            raise ValueError("Both place_id and amenity_id are required")

        # Vérifier que place et amenity existent
        place = self.get(Place, place_id)
        amenity = self.get(Amenity, amenity_id)

        if not place or not amenity:
            raise ValueError("Place or Amenity not found")

        # Vérifier que l'utilisateur a les droits sur la place
        if not place.can_be_managed_by(user_id, is_admin):
            raise ValueError("You cannot modify this place! 👻")

        # Créer le lien
        link = PlaceAmenity(place_id=place_id, amenity_id=amenity_id)
        return link.save()
