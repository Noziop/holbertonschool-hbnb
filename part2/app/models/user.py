from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'username': self.username,
            'email': self.email
        })
        return user_dict