# app/tests/test_spooky/test_models/test_placeamenity.py
"""Test module for our PlaceAmenity model! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture(autouse=True)
def setup_repository():
    """Setup clean repository for each test! 🏰"""
    from app.models.placeamenity import PlaceAmenity
    from app.persistence.repository import InMemoryRepository
    
    repo = InMemoryRepository()
    repo._storage.clear()
    PlaceAmenity.repository = repo
    
    yield repo
    
    repo._storage.clear()

@pytest.fixture
def test_place():
    """Create a test place! 🏰"""
    from app.models.place import Place
    from app.models.user import User
    
    # Create owner
    owner = User(
        username="ghost_owner",
        email="owner@haunted.com",
        password="Ghost123!@#",
        first_name="Ghost",
        last_name="Owner"
    )
    owner.save()
    
    # Create place
    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=owner.id,
        price_by_night=100.0
    )
    place.save()
    return place

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

def test_placeamenity_creation(test_place, test_amenity):
    """Test basic PlaceAmenity creation! 🎭"""
    from app.models.placeamenity import PlaceAmenity
    
    link = PlaceAmenity(
        place_id=test_place.id,
        amenity_id=test_amenity.id
    )
    
    assert link.place_id == test_place.id
    assert link.amenity_id == test_amenity.id
    assert hasattr(link, 'id')
    assert hasattr(link, 'created_at')
    assert hasattr(link, 'updated_at')
    assert link.is_active is True
    assert link.is_deleted is False

def test_placeamenity_validation():
    """Test PlaceAmenity validation rules! 🎭"""
    from app.models.placeamenity import PlaceAmenity
    
    # Test invalid place_id
    with pytest.raises(ValueError):
        PlaceAmenity(
            place_id="invalid-id",
            amenity_id=str(uuid.uuid4())
        )
    
    # Test invalid amenity_id
    with pytest.raises(ValueError):
        PlaceAmenity(
            place_id=str(uuid.uuid4()),
            amenity_id="invalid-id"
        )

def test_placeamenity_to_dict(test_place, test_amenity):
    """Test PlaceAmenity to_dict transformation! 📝"""
    from app.models.placeamenity import PlaceAmenity
    
    link = PlaceAmenity(
        place_id=test_place.id,
        amenity_id=test_amenity.id
    )
    link.save()
    
    link_dict = link.to_dict()
    
    assert isinstance(link_dict, dict)
    assert link_dict['place_id'] == test_place.id
    assert link_dict['amenity_id'] == test_amenity.id
    assert 'id' in link_dict
    assert 'created_at' in link_dict
    assert 'updated_at' in link_dict
    assert 'is_active' in link_dict
    assert 'is_deleted' in link_dict