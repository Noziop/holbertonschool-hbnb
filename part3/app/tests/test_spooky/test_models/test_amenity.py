# app/tests/test_spooky/test_models/test_amenity.py
"""Test module for our Amenity model! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture(autouse=True)
def setup_repository():
    """Setup clean repository for each test! 🏰"""
    from app.models.amenity import Amenity
    from app.persistence.repository import InMemoryRepository
    
    repo = InMemoryRepository()
    repo._storage.clear()
    Amenity.repository = repo
    
    yield repo
    
    repo._storage.clear()

@pytest.fixture
def test_amenity():
    """Create a test amenity! 🎭"""
    from app.models.amenity import Amenity
    
    amenity = Amenity(
        name="Ghost Detector",
        description="Detects supernatural activity!"
    )
    amenity.save()
    return amenity

def test_amenity_creation():
    """Test basic Amenity creation! 🎭"""
    from app.models.amenity import Amenity
    
    amenity = Amenity(
        name="Spirit Box",
        description="Communicate with spirits!"
    )
    
    assert amenity.name == "Spirit Box"
    assert amenity.description == "Communicate with spirits!"
    assert hasattr(amenity, 'id')
    assert hasattr(amenity, 'created_at')
    assert hasattr(amenity, 'updated_at')
    assert amenity.is_active is True
    assert amenity.is_deleted is False

def test_amenity_validation():
    """Test Amenity validation rules! 🎭"""
    from app.models.amenity import Amenity
    
    # Test empty name
    with pytest.raises(ValueError):
        Amenity(name="", description="Test")
    
    # Test invalid name characters
    with pytest.raises(ValueError):
        Amenity(name="Invalid@Name!", description="Test")
    
    # Test non-string description
    with pytest.raises(ValueError):
        Amenity(name="Valid Name", description=123)

def test_amenity_update(test_amenity):
    """Test Amenity update functionality! 🔄"""
    # Update name and description
    test_amenity.update({
        'name': "EMF Reader",
        'description': "Updated description"
    })
    
    assert test_amenity.name == "EMF Reader"
    assert test_amenity.description == "Updated description"
    
    # Test duplicate name
    other_amenity = test_amenity.__class__(
        name="Other Amenity",
        description="Test"
    )
    other_amenity.save()
    
    with pytest.raises(ValueError):
        other_amenity.update({'name': "EMF Reader"})

def test_amenity_to_dict(test_amenity):
    """Test Amenity to_dict transformation! 📝"""
    amenity_dict = test_amenity.to_dict()
    
    assert isinstance(amenity_dict, dict)
    assert amenity_dict['name'] == "Ghost Detector"
    assert amenity_dict['description'] == "Detects supernatural activity!"
    assert 'id' in amenity_dict
    assert 'created_at' in amenity_dict
    assert 'updated_at' in amenity_dict
    assert 'is_active' in amenity_dict
    assert 'is_deleted' in amenity_dict

def test_amenity_get_places(test_amenity):
    """Test getting places with this amenity! 🏰"""
    places = test_amenity.get_places()
    assert isinstance(places, list)