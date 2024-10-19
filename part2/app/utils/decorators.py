from functools import wraps
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity

def validate_entity_exists(entity_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, entity_id, *args, **kwargs):
            if entity_type == 'user':
                entity = User.get_by_id(entity_id)
            elif entity_type == 'place':
                entity = Place.get_by_id(entity_id)
            elif entity_type == 'amenity':
                entity = Amenity.get_by_id(entity_id)
            else:
                raise ValueError(f"Unknown entity type: {entity_type}")
            
            if not entity:
                raise ValueError(f"No {entity_type} found with id: {entity_id}")
            return func(self, entity_id, *args, **kwargs)
        return wrapper
    return decorator

def validate_user_exists(func):
    @wraps(func)
    def wrapper(self, user_id, *args, **kwargs):
        user = User.get_by_id(user_id)
        if not user:
            raise ValueError(f"No user found with id: {user_id}")
        return func(self, user_id, *args, **kwargs)
    return wrapper