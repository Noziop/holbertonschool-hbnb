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
            return None
        return obj

    def update(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key not in ['id', 'created_at']:
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        raise AttributeError(f"Invalid attribute: {key}")
        else:
            # Si data n'est pas un dictionnaire, on suppose que c'est un objet
            for key in dir(data):
                if not key.startswith('_') and key not in ['id', 'created_at', 'update']:
                    if hasattr(self, key):
                        setattr(self, key, getattr(data, key))
                    else:
                        raise AttributeError(f"Invalid attribute: {key}")
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def save(self):
        self.updated_at = datetime.now(timezone.utc)
        self.repository.update(self.id, self.to_dict())