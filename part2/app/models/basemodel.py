import uuid
from datetime import datetime, timezone

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def save(self):
        self.updated_at = datetime.now(timezone.utc)

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def __eq__(self, other):
        if isinstance(other, BaseModel):
            return self.id == other.id
        return False