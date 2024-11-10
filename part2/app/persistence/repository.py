from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Union

T = TypeVar("T", bound="BaseModel")


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(
        self, multiple: bool = False, **kwargs: Any
    ) -> Union[Any, List[Any]]:
        """
        Get objects by attributes. Like a haunted treasure hunt! 👻

        Args:
            multiple: Summon one spirit or the whole graveyard? 🪦
            **kwargs: Your spooky search criteria (each one darker than the last!)

        WHY:
            Because searching through objects is like looking for ghosts:
            You better have the right tools! 🔮

        BEWARE MORTAL, THIS CODE IS CURSED! 💀
        """
        pass


class InMemoryRepository(Repository):
    _instances = {}  # Stockage par ID
    _instances_by_type = {}  # Stockage par type

    def __init__(self):
        self._storage = {}

    @classmethod
    def clear_all(cls):
        """Clean our haunted storage! 🧹"""
        print("🧹 Starting deep cleanup...")  # Debug
        # Vider complètement les dictionnaires
        cls._instances.clear()
        cls._instances_by_type.clear()

        # Vérification
        print(f"📊 After cleanup:")
        print(f"_instances: {cls._instances}")
        print(f"_instances_by_type: {cls._instances_by_type}")
        print("✨ Deep cleanup complete!")

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(
        self, multiple: bool = False, **kwargs: Any
    ) -> Union[Any, List[Any]]:
        """
        Get objects by attributes. Summoning entities from the storage beyond! 👻

        Args:
            multiple: Want one ghost or a whole haunted house? 🏚️
            **kwargs: The dark specifications (each more cursed than the last!)

        WHY:
            Because searching through storage is like necromancy:
            You gotta be specific with your summons! 🧙‍♀️

        THE SPIRITS ARE WATCHING! 🦇
        """
        results = [
            obj
            for obj in self._storage.values()
            if all(getattr(obj, attr, None) == value for attr, value in kwargs.items())
        ]

        if not results:
            return [] if multiple else None

        return results if multiple else results[0]
