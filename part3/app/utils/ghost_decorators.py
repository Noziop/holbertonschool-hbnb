# app/utils/ghost_decorators.py
"""Decorators for our haunted models! 👻"""
from datetime import datetime, timezone
from functools import wraps
from typing import Optional, List, Type

def spell_book(
    validate: bool = True,
    timestamp: bool = True,
    to_dict_exclude: Optional[List[str]] = None
):
    """Cast multiple spells on your model class! 🎭
    
    This decorator combines multiple model enhancements:
    - Validation spell (validate_ghost) 📜
    - Timestamp tracking magic ⌛
    - Dictionary transformation enchantment 🔮
    
    Args:
        validate (bool): Apply validation spell
        timestamp (bool): Apply timestamp tracking
        to_dict_exclude (List[str]): Fields to exclude from dict transformation
    """
    def decorator(cls: Type) -> Type:
        # Cast validation spell if requested
        if validate:
            from .ghost_validator import validate_ghost
            cls = validate_ghost(cls)
        
        # Cast timestamp spell if requested
        if timestamp:
            def update_timestamp(method):
                @wraps(method)
                def wrapper(self, *args, **kwargs):
                    result = method(self, *args, **kwargs)
                    # Ne pas mettre à jour le timestamp pour __init__
                    if method.__name__ != '__init__':
                        self.updated_at = datetime.now(timezone.utc)
                    return result
                return wrapper
            
            # Enchant all public methods except __init__
            for attr_name, attr_value in cls.__dict__.items():
                if (callable(attr_value) and 
                    not attr_name.startswith('_') and 
                    attr_name != '__init__'):
                    setattr(cls, attr_name, update_timestamp(attr_value))
        
        # Cast dictionary transformation spell if requested
        if to_dict_exclude is not None:
            def to_dict_method(self):
                """Transform model into a dictionary representation"""
                data = {}
                for key, value in self.__dict__.items():
                    if key not in to_dict_exclude and not key.startswith('_'):
                        if isinstance(value, datetime):
                            data[key] = value.isoformat()
                        else:
                            data[key] = value
                return data
            
            cls.to_dict = to_dict_method
        
        return cls
    
    return decorator