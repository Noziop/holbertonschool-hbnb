import uuid
from datetime import datetime, timezone
from app.persistence.repository import InMemoryRepository

class BaseModel:
    repository = InMemoryRepository()

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        cls.repository.add(instance)
        return instance

    @classmethod
    def get_by_id(cls, id):
        obj = cls.repository.get(id)
        if obj is None:
            raise ValueError(f"No {cls.__name__} found with id: {id}")
        return obj

    def update(self, data):
        try:
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self.updated_at = datetime.now(timezone.utc)
            self.repository.update(self.id, self)
        except Exception as e:
            raise ValueError(f"Update failed: {str(e)}")

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def save(self):
        self.updated_at = datetime.now(timezone.utc)
        self.repository.update(self.id, self)