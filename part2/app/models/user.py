from app.persistence.repository import InMemoryRepository
from app.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    repository = InMemoryRepository()

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)

    @classmethod
    def create(cls, username, email, password):
        user = cls(username, email, password)
        cls.repository.add(user)
        return user

    @classmethod
    def get_by_username(cls, username):
        return cls.repository.get_by_attribute('username', username)

    @classmethod
    def get_by_id(cls, user_id):
        user = cls.repository.get(user_id)
        if user is None:
            raise ValueError(f"No user found with id: {user_id}")
        return user

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self.repository.update(self.id, self)

    def delete(self):
        self.repository.delete(self.id)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }