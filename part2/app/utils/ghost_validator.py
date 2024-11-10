# app/utils/ghost_validator.py
"""Ghost validation module for our haunted models! 👻"""
from datetime import datetime
from functools import wraps
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Type, Union

from .cursed_errors import ValidationError

if TYPE_CHECKING:
    from app.models.amenity import Amenity
    from app.models.basemodel import BaseModel
    from app.models.place import Place
    from app.models.review import Review
    from app.models.user import User

# Types personnalisés
ValidationResult = Tuple[bool, Optional[str]]
ValidationRules = Dict[str, Dict[str, Any]]


def validate_ghost(cls: Type) -> Type:
    """Decorator to add validation capabilities to a class! 🎭"""

    def validate_relationship(entity_type: str, entity_id: str) -> ValidationResult:
        """Validate that a related entity exists"""
        if entity_type == "User":
            from app.models.user import User

            return True, None
        elif entity_type == "Place":
            from app.models.place import Place

            return True, None
        elif entity_type == "Review":
            from app.models.review import Review

            return True, None
        elif entity_type == "Amenity":
            from app.models.amenity import Amenity

            return True, None
        return False, f"Unknown entity type: {entity_type}"

    def validate_and_set(self, partial: bool = False, **kwargs: Dict[str, Any]) -> None:
        """Validate and set attributes based on validation rules"""
        errors: List[str] = []
        validated_data: Dict[str, Any] = {}

        # Pour l'initialisation, on garde les valeurs existantes
        if hasattr(self, "id"):
            for field in self.__validation_rules__.keys():
                if hasattr(self, field):
                    validated_data[field] = getattr(self, field)

        # Set default values first
        for field, rules in self.__validation_rules__.items():
            if "default" in rules and field not in kwargs:
                validated_data[field] = rules["default"]

        # Check required fields only if not partial
        if not partial:
            for field, rules in self.__validation_rules__.items():
                if rules.get("required", False) and field not in kwargs:
                    errors.append(f"Field '{field}' is required")

        # Validate each field that has rules
        for field, value in kwargs.items():
            if field in self.__validation_rules__:
                rules = self.__validation_rules__[field]

                # Validate relationship first
                if rules.get("exists"):
                    entity_type = rules["exists"]
                    is_valid, error = validate_relationship(entity_type, value)
                    if not is_valid:
                        errors.append(f"Invalid {field}: {error}")
                        continue

                # Type validation
                expected_type = rules.get("type")
                if expected_type:
                    # Handle tuple of types (like (int, float))
                    if isinstance(expected_type, tuple):
                        if not isinstance(value, expected_type):
                            types_str = " or ".join(t.__name__ for t in expected_type)
                            errors.append(
                                f"Field '{field}' must be of type {types_str}"
                            )
                    elif not isinstance(value, expected_type):
                        errors.append(
                            f"Field '{field}' must be of type {expected_type.__name__}"
                        )

                # String validation
                if isinstance(value, str):
                    min_length = rules.get("min_length")
                    max_length = rules.get("max_length")
                    pattern = rules.get("pattern")

                    if min_length and len(value) < min_length:
                        errors.append(
                            f"Field '{field}' must be at least {min_length} characters"
                        )
                    if max_length and len(value) > max_length:
                        errors.append(
                            f"Field '{field}' must be at most {max_length} characters"
                        )
                    if pattern:
                        import re

                        if not re.match(pattern, value):
                            errors.append(f"Field '{field}' has invalid format")

                # Numeric validation
                if isinstance(value, (int, float)):
                    min_value = rules.get("min_value")
                    max_value = rules.get("max_value")

                    if min_value is not None and value < min_value:
                        errors.append(
                            f"Field '{field}' must be greater than {min_value}"
                        )
                    if max_value is not None and value > max_value:
                        errors.append(f"Field '{field}' must be less than {max_value}")

                # Choice validation
                choices = rules.get("choices")
                if choices and value not in choices:
                    errors.append(
                        f"Field '{field}' must be one of: {', '.join(choices)}"
                    )

                # If field passes validation, add to validated data
                validated_data[field] = value

        # If there are errors, raise ValidationError
        if errors:
            raise ValidationError("\n".join(errors))

        # Set validated attributes
        for field, value in validated_data.items():
            setattr(self, field, value)

    # Add validation methods to class
    setattr(cls, "validate_and_set", validate_and_set)
    setattr(cls, "validate_relationship", staticmethod(validate_relationship))
    return cls
