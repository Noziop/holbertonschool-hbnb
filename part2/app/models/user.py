#!usr/bin/python3
'''Module that creates a user class'''


from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User:
    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }