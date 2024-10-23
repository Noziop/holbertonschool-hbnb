from abc import ABC, abstractmethod
from typing import Any, Union, List, TypeVar


T = TypeVar('T', bound='BaseModel')

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
        self, 
        attr: str, 
        value: Any, 
        multiple: bool = False
    ) -> Union[Any, List[Any]]:
        """
        Get objects by attribute. Abstract but make it fashion! 💅
        
        Args:
            attr: The attribute to search by (like a desperate housewife during the sales!)
            value: The value to match (standards are high, honey!)
            multiple: If True, returns all matches (like your dating history!)

        WHY: 
            Because repeating yourself is like wearing the same outfit twice:
            YOU DON'T! 💅

        WATCH ME CODE, DARLING! 💋
        """
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    @classmethod
    def clear_all(cls):
        cls.data = {}

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
        self, 
        attr: str, 
        value: Any, 
        multiple: bool = False
    ) -> Union[Any, List[Any]]:
        """
        Get objects by attribute. Serving looks from storage! 💅
        
        Args:
            attr: The attribute to search by (like a desperate housewife during the sales!)
            value: The value to match (standards are high, honey!)
            multiple: If True, returns all matches (like your dating history!)

        WHY: 
            Because repeating yourself is like wearing the same outfit twice:
            YOU DON'T! 💅

        WATCH ME CODE, DARLING! 💋
        """
        results = [
            obj for obj in self._storage.values() 
            if getattr(obj, attr, None) == value
        ]
        
        if not results:
            return [] if multiple else None
            
        return results if multiple else results[0]