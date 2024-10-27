"""Test module for our ghost validation system! 👻"""
import pytest
from datetime import datetime
from app.utils.cursed_errors import ValidationError

def test_user_validation():
    """Test validation for User model! 🧙‍♀️"""
    from app.utils.ghost_validator import validate_ghost
    
    @validate_ghost
    class TestUser:
        __validation_rules__ = {
            'username': {
                'type': str,
                'required': True,
                'min_length': 6,
                'max_length': 18,
                'unique': True
            },
            'email': {
                'type': str,
                'required': True,
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'unique': True
            },
            'password': {
                'type': str,
                'required': True,
                'min_length': 8,
                'pattern': r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
            },
            'first_name': {
                'type': str,
                'required': True,
                'min_length': 2,
                'max_length': 18
            },
            'last_name': {
                'type': str,
                'required': True,
                'min_length': 2,
                'max_length': 36
            },
            'phone_number': {
                'type': str,
                'required': False,
                'pattern': r'^\+?[\d\s-]{10,15}$'  # Plus strict !
            },
            'address': {
                'type': str,
                'required': False,
                'max_length': 64  # Réduit de 256
            },
            'postal_code': {
                'type': str,
                'required': False,
                'pattern': r'^\d{5}$'
            },
            'city': {
                'type': str,
                'required': False,
                'max_length': 36  # Réduit de 128
            },
            'country': {
                'type': str,
                'required': False,
                'max_length': 36  # Réduit de 128
            },
            'is_admin': {
                'type': bool,
                'required': False,
                'default': False
            },
            'is_active': {
                'type': bool,
                'required': False,
                'default': True
            }
        }

def test_place_validation():
    """Test validation for Place model! 🏰"""
    from app.utils.ghost_validator import validate_ghost

    @validate_ghost
    class TestPlace:
        __validation_rules__ = {
            'name': {
                'type': str,
                'required': True,
                'min_length': 3,
                'max_length': 64
            },
            'description': {
                'type': str,
                'required': False,
                'max_length': 512
            },
            'number_rooms': {
                'type': int,
                'required': True,
                'min_value': 0
            },
            'number_bathrooms': {
                'type': int,
                'required': True,
                'min_value': 0
            },
            'max_guest': {
                'type': int,
                'required': True,
                'min_value': 0
            },
            'price_by_night': {
                'type': (int, float),  # Accepte les deux types
                'required': True,
                'min_value': 0
            },
            'latitude': {
                'type': (int, float),  # Accepte les deux types
                'required': False,
                'min_value': -90,
                'max_value': 90
            },
            'longitude': {
                'type': (int, float),  # Accepte les deux types
                'required': False,
                'min_value': -180,
                'max_value': 180
            },
            'city': {
                'type': str,
                'required': True,
                'max_length': 128
            },
            'country': {
                'type': str,
                'required': True,
                'max_length': 128
            },
            'owner_id': {
                'type': str,
                'required': True,
                'exists': 'User'
            },
            'address': {
                'type': str,
                'required': True,
                'max_length': 256
            },
            'postal_code': {
                'type': str,
                'required': True,
                'pattern': r'^\d{5}$'
            },
            'is_available': {
                'type': bool,
                'required': False,
                'default': True
            },
            'status': {
                'type': str,
                'required': False,
                'choices': ['available', 'booked', 'maintenance']
            },
            'minimum_stay': {
                'type': int,
                'required': False,
                'min_value': 1
            },
            'property_type': {
                'type': str,
                'required': True,
                'choices': ['house', 'apartment', 'room', 'other']
            },
            'is_active': {
                'type': bool,
                'required': False,
                'default': True
            }
        }

def test_amenity_validation():
    """Test validation for Amenity model! 🛋️"""
    from app.utils.ghost_validator import validate_ghost

    @validate_ghost
    class TestAmenity:
        __validation_rules__ = {
            'id': {
                'type': str,
                'required': True,
                'unique': True
            },
            'name': {
                'type': str,
                'required': True,
                'min_length': 2,
                'max_length': 128,
                'unique': True
            },
            'description': {
                'type': str,
                'required': False,
                'max_length': 1024
            },
            'is_active': {
                'type': bool,
                'required': False,
                'default': True
            }
        }

def test_review_validation():
    """Test validation for Review model! 📝"""
    from app.utils.ghost_validator import validate_ghost

    @validate_ghost
    class TestReview:
        __validation_rules__ = {
            'place_id': {
                'type': str,
                'required': True,
                'exists': 'Place'
            },
            'user_id': {
                'type': str,
                'required': True,
                'exists': 'User'
            },
            'text': {
                'type': str,
                'required': True,
                'min_length': 1,
                'max_length': 1024
            },
            'rating': {
                'type': int,
                'required': True,
                'min_value': 1,
                'max_value': 5
            },
            'is_active': {
                'type': bool,
                'required': False,
                'default': True
            }
        }

def test_basemodel_validation():
    """Test validation for BaseModel! 👻"""
    from app.utils.ghost_validator import validate_ghost
    import uuid
    from datetime import datetime, timezone
    
    @validate_ghost
    class TestBaseModel:
        __validation_rules__ = {
            'id': {
                'type': str,
                'required': True,
                'pattern': r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'  # UUID v4 pattern
            },
            'created_at': {
                'type': datetime,
                'required': True
            },
            'updated_at': {
                'type': datetime,
                'required': True
            },
            'is_active': {
                'type': bool,
                'required': False,
                'default': True
            }
        }
        
        def __init__(self, **kwargs):
            # Si pas d'ID fourni, en créer un
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            
            # Si pas de timestamps fournis, les créer
            now = datetime.now(timezone.utc)
            if 'created_at' not in kwargs:
                kwargs['created_at'] = now
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = now
                
            self.validate_and_set(**kwargs)
    
    # Test création basique
    base = TestBaseModel()
    assert base.id is not None
    assert base.created_at is not None
    assert base.updated_at is not None
    assert base.is_active is True
    
    # Test avec valeurs fournies
    custom_id = str(uuid.uuid4())
    custom_time = datetime.now(timezone.utc)
    base = TestBaseModel(
        id=custom_id,
        created_at=custom_time,
        updated_at=custom_time,
        is_active=False
    )
    assert base.id == custom_id
    assert base.created_at == custom_time
    assert base.updated_at == custom_time
    assert base.is_active is False
    
    # Test avec ID invalide
    with pytest.raises(ValidationError):
        TestBaseModel(id="not-a-uuid")

def test_relationship_validation():
    """Test that relationships are properly validated! 🔗"""
    from app.utils.ghost_validator import validate_ghost
    
    @validate_ghost
    class TestReview:
        __validation_rules__ = {
            'user_id': {
                'type': str,
                'required': True,
                'exists': 'User'
            },
            'place_id': {
                'type': str,
                'required': True,
                'exists': 'Place'
            },
            'text': {
                'type': str,
                'required': True,
                'min_length': 1,
                'max_length': 512
            }
        }
        
        def __init__(self, **kwargs):
            self.validate_and_set(**kwargs)
    
    # Test valid relationships
    review = TestReview(
        user_id="valid_user_id",
        place_id="valid_place_id",
        text="Great haunted place!"
    )
    
    # Test invalid user_id
    with pytest.raises(ValidationError) as e:
        TestReview(
            user_id="invalid_user_id",
            place_id="valid_place_id",
            text="Spooky review!"
        )
    assert "Invalid user_id" in str(e.value)
    
    # Test invalid place_id
    with pytest.raises(ValidationError) as e:
        TestReview(
            user_id="valid_user_id",
            place_id="invalid_place_id",
            text="Ghost review!"
        )
    assert "Invalid place_id" in str(e.value)

def test_multiple_types_validation():
    """Test validation with multiple allowed types! 🎭"""
    from app.utils.ghost_validator import validate_ghost
    
    @validate_ghost
    class TestPlace:
        __validation_rules__ = {
            'price_by_night': {
                'type': (int, float),
                'required': True,
                'min_value': 0
            },
            'latitude': {
                'type': (int, float),
                'required': False,
                'min_value': -90,
                'max_value': 90
            }
        }
        
        def __init__(self, **kwargs):
            self.validate_and_set(**kwargs)
    
    # Test with integer
    place1 = TestPlace(price_by_night=100)
    assert place1.price_by_night == 100
    
    # Test with float
    place2 = TestPlace(price_by_night=99.99, latitude=45.5)
    assert place2.price_by_night == 99.99
    assert place2.latitude == 45.5
    
    # Test invalid type
    with pytest.raises(ValidationError) as e:
        TestPlace(price_by_night="100")  # String instead of number
    assert "must be of type int or float" in str(e.value)
    
    # Test invalid value
    with pytest.raises(ValidationError) as e:
        TestPlace(price_by_night=-10)  # Negative price
    assert "must be greater than 0" in str(e.value)