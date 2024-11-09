# app/utils/phantom_types.py
"""Type definitions for our haunted app! 👻"""
from typing import TypeVar, Dict, Any, Union, Optional, Callable, Tuple
from datetime import datetime

# Type variables for our models
UserType = TypeVar('UserType', bound='User')
PlaceType = TypeVar('PlaceType', bound='Place')
ReviewType = TypeVar('ReviewType', bound='Review')
AmenityType = TypeVar('AmenityType', bound='Amenity')

# Common types
ValidationRules = Dict[str, Dict[str, Any]]
NumericType = Union[int, float]
DateTimeType = Union[datetime, str]

# Validation types
ValidatorFunction = Callable[[Any], bool]
ValidationResult = Tuple[bool, Optional[str]]