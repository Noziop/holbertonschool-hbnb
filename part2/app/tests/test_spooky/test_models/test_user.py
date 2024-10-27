# app/tests/test_spooky/test_models/test_user.py
"""Test module for our UserModel! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture
def repository():
    """Create a fresh repository for each test! 🏰"""
    from app.persistence.repository import InMemoryRepository
    return InMemoryRepository()

def test_user_creation():
    """Test basic User creation with default values! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly"
    )
    
    # Vérification des attributs requis
    assert hasattr(user, 'id')
    assert isinstance(user.id, str)
    assert uuid.UUID(user.id)
    
    assert hasattr(user, 'username')
    assert user.username == "friendly_ghost"
    
    assert hasattr(user, 'email')
    assert user.email == "ghost@haunted.com"
    
    assert hasattr(user, 'password_hash')  # On vérifie le hash, pas le password
    
    assert hasattr(user, 'first_name')
    assert user.first_name == "Casper"
    
    assert hasattr(user, 'last_name')
    assert user.last_name == "Friendly"
    
    # Vérification des attributs par défaut
    assert hasattr(user, 'is_active')
    assert user.is_active is True
    
    assert hasattr(user, 'is_admin')
    assert user.is_admin is False

def test_user_with_optional_attributes():
    """Test User creation with optional attributes! 🎭"""
    from app.models.user import User
    
    user = User(
        username="spooky_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly",
        address="13 Haunted Street",
        postal_code="13666",
        city="Ghostville",
        phone="+1-666-GHOST"
    )
    
    assert user.username == "spooky_ghost"
    assert user.address == "13 Haunted Street"
    assert user.postal_code == "13666"
    assert user.city == "Ghostville"
    assert user.phone == "+1-666-GHOST"

def test_user_update():
    """Test User update! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly"
    )
    
    original_updated_at = user.updated_at
    
    # Update required fields
    user.update({
        'username': 'super_ghost',
        'first_name': 'Super',
        'last_name': 'Ghost'
    })
    
    assert user.username == 'super_ghost'
    assert user.first_name == 'Super'
    assert user.last_name == 'Ghost'
    assert user.updated_at > original_updated_at
    
    # Update optional fields
    user.update({
        'address': '666 Spooky Lane',
        'phone': '+1-666-BOO'
    })
    
    assert user.address == '666 Spooky Lane'
    assert user.phone == '+1-666-BOO'

def test_user_to_dict():
    """Test User to_dict transformation! 🎭"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",  # Mot de passe plus long
        first_name="Casper",
        last_name="Friendly",
        address="13 Haunted Street",
        phone="+1-666-GHOST"
    )
    
    user_dict = user.to_dict()
    
    assert isinstance(user_dict, dict)
    assert 'id' in user_dict
    assert 'username' in user_dict
    assert 'email' in user_dict
    assert 'password' not in user_dict  # Password should not be in dict
    assert 'password_hash' not in user_dict  # Hash should not be in dict
    assert 'first_name' in user_dict
    assert 'last_name' in user_dict
    assert 'address' in user_dict
    assert 'phone' in user_dict
    assert 'created_at' in user_dict
    assert 'updated_at' in user_dict
    assert 'is_active' in user_dict
    assert 'is_admin' in user_dict

def test_user_account_states():
    """Test User account states (pause, reactivate)! 🌙"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Test pause account
    assert user.pause_account() is True
    assert user.is_active is False
    assert user.is_deleted is False
    
    # Test reactivate account
    assert user.reactivate_account() is True
    assert user.is_active is True
    assert user.is_deleted is False

def test_user_delete():
    """Test User deletion with related entities! ⚰️"""
    from app.models.user import User
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Test soft delete
    assert user.delete() is True
    assert user.is_active is False
    assert user.is_deleted is True
    
    # Test cannot reactivate deleted account
    with pytest.raises(ValueError):
        user.reactivate_account()

@pytest.mark.skip(reason="Place not implemented yet")
def test_user_places_visibility():
    """Test User places visibility when account is paused! 🏠"""
    from app.models.user import User
    from app.models.place import Place
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Create a place for the user
    place = Place(
        name="Haunted Mansion",
        owner_id=user.id,
        description="A spooky place",
        price_per_night=100
    )
    place.save()
    
    # Test place visibility when account is paused
    user.pause_account()
    assert place.is_active is False
    
    # Test place visibility when account is reactivated
    user.reactivate_account()
    assert place.is_active is True

@pytest.mark.skip(reason="Review not implemented yet")
def test_user_delete_with_reviews():
    """Test User deletion with reviews! 📝"""
    from app.models.user import User
    from app.models.review import Review
    
    user = User(
        username="friendly_ghost",
        email="ghost@haunted.com",
        password="Boo123!@#",
        first_name="Casper",
        last_name="Friendly"
    )
    user.save()
    
    # Create a review
    review = Review(
        user_id=user.id,
        place_id="some-place-id",
        text="Spooky place!"
    )
    review.save()
    
    # Test soft delete
    user.delete()
    
    # Check if review is anonymized
    updated_review = Review.get_by_id(review.id)
    assert updated_review.user_id is None