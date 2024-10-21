import uuid
import datetime as dt
from app.persistence.repository import InMemoryRepository
from app.utils import *

class BaseModel:
    repository = InMemoryRepository()

    @magic_wand(validate_input(BaseModelValidation))
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        print(f'ID: {self.id}')
        date = dt.datetime.now(dt.timezone.utc)
        print(f'Date: {date}')
        self.created_at = dt.datetime.now(dt.timezone.utc)
        print(f'Created At: {self.created_at}')
        self.updated_at = dt.datetime.now(dt.timezone.utc)
        print(f'Updated At: {self.updated_at}')
        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @classmethod
    @magic_wand()
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls.repository.add(instance)
        return instance

    @classmethod
    @magic_wand(validate_input({'id': str}))
    def get_by_id(cls, id):
        obj = cls.repository.get(id)
        if obj is None:
            raise ValueError(f"No {cls.__name__} found with id: {id}")
        return obj

    @classmethod
    @magic_wand(validate_input({'name': str}))
    def get_by_name(cls, name):
        return cls.repository.get_by_attribute('name', name)
    
    @classmethod
    @magic_wand()
    def get_all(cls):
        return cls.repository.get_all()

    @magic_wand(validate_input({'data': dict}))
    def update(self, data):
        for key, value in data.items():
            if key in ['id', 'created_at']:
                raise ValueError(f"Cannot update {key} attribute")
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

    @magic_wand()
    def delete(self):
        if not self.repository.get(self.id):
            raise ValueError(f"No {self.__class__.__name__} found with id: {self.id}")
        self.repository.delete(self.id)
        return True

    @magic_wand(update_timestamp)
    def save(self):
        try:
            data = self.to_dict()
            data.pop('id', None)
            data.pop('created_at', None)
            self.repository.update(self.id, data)
        except Exception as e:
            raise ValueError(f"Failed to save: {str(e)}")

    @magic_wand()
    @to_dict(exclude=[])
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }