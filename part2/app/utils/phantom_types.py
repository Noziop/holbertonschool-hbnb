# app/utils/phantom_types.py
"""Type definitions for our haunted app! 👻"""
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

# Type variables for our models
UserType = TypeVar("UserType", bound="User")
PlaceType = TypeVar("PlaceType", bound="Place")
ReviewType = TypeVar("ReviewType", bound="Review")
AmenityType = TypeVar("AmenityType", bound="Amenity")

# Common types
ValidationRules = Dict[str, Dict[str, Any]]
NumericType = Union[int, float]
DateTimeType = Union[datetime, str]

# Validation types
ValidatorFunction = Callable[[Any], bool]
ValidationResult = Tuple[bool, Optional[str]]
