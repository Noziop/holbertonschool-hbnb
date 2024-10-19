import uuid
from datetime import datetime, timezone
from app.persistence.repository import InMemoryRepository
from app.utils.magic_wands import log_action, error_handler, validate_input, update_timestamp, to_dict_decorator

class BaseModel:
    repository = InMemoryRepository()

    @log_action
    @error_handler
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at']:
                setattr(self, key, datetime.fromisoformat(value))
            else:
                setattr(self, key, value)

    @classmethod
    @log_action
    @error_handler
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls.repository.add(instance)
        return instance

    @classmethod
    @log_action
    @error_handler
    @validate_input(id=str)
    def get_by_id(cls, id):
        obj = cls.repository.get(id)
        if obj is None:
            raise ValueError(f"No {cls.__name__} found with id: {id}")
        return obj

    @classmethod
    @log_action
    @error_handler
    @validate_input(name=str)
    def get_by_name(cls, name):
        return cls.repository.get_by_attribute('name', name)
    
    @classmethod
    @log_action
    @error_handler
    def get_all(cls):
        return cls.repository.get_all()

    @log_action
    @error_handler
    @update_timestamp
    @validate_input(data=dict)
    def update(self, data):
        for key, value in data.items():
            if key in ['id', 'created_at']:
                raise ValueError(f"Cannot update {key} attribute")
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

    @log_action
    @error_handler
    def delete(self):
        if not self.repository.get(self.id):
            raise ValueError(f"No {self.__class__.__name__} found with id: {self.id}")
        self.repository.delete(self.id)

    @log_action
    @error_handler
    @update_timestamp
    def save(self):
        try:
            data = self.to_dict()
            data.pop('id', None)
            data.pop('created_at', None)
            self.repository.update(self.id, data)
        except Exception as e:
            raise ValueError(f"Failed to save: {str(e)}")

    @to_dict_decorator()
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }