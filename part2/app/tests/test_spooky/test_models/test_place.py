# app/tests/test_spooky/test_models/test_place.py
"""Test module for our Place model! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture
def repository():
    """Create a fresh repository for each test! 🏰"""
    from app.persistence.repository import InMemoryRepository
    repo = InMemoryRepository()
    # Clear any existing data
    repo._storage.clear()
    return repo

@pytest.fixture
def test_place(repository):
    """Create a test place for each test! 🏰"""
    from app.models.place import Place
    Place.repository = repository  # Use clean repository
    
    place = Place(
        name="Haunted Manor",
        description="A spooky place with lots of ghosts!",
        owner_id=str(uuid.uuid4()),
        price_by_night=100.0,
        number_rooms=3,
        number_bathrooms=2,
        max_guest=6,
        city="Ghostville",
        country="Spookyland"
    )
    place.save()
    return place

def test_place_creation():
    """Test basic Place creation with default values! 🎭"""
    from app.models.place import Place
    
    place = Place(
        name="Haunted Manor",
        description="A spooky place with lots of ghosts!",
        owner_id=str(uuid.uuid4()),
        price_by_night=100.0
    )
    
    # Required attributes
    assert place.name == "Haunted Manor"
    assert place.description == "A spooky place with lots of ghosts!"
    assert isinstance(place.owner_id, str)
    assert place.price_by_night == 100.0
    
    # Default values
    assert place.number_rooms == 1
    assert place.number_bathrooms == 1
    assert place.max_guest == 2
    assert place.latitude is None
    assert place.longitude is None
    assert place.city == ""
    assert place.country == ""
    assert place.status == "active"
    assert place.property_type == "apartment"
    assert place.minimum_stay == 1

def test_place_with_all_attributes():
    """Test Place creation with all attributes! 🏰"""
    from app.models.place import Place
    
    place = Place(
        name="Luxury Ghost Manor",
        description="The most haunted mansion in town!",
        owner_id=str(uuid.uuid4()),
        price_by_night=200.0,
        number_rooms=5,
        number_bathrooms=3,
        max_guest=10,
        latitude=45.5,
        longitude=-73.5,
        city="Ghostville",
        country="Spookyland",
        status="active",
        property_type="villa",
        minimum_stay=2
    )
    
    assert place.name == "Luxury Ghost Manor"
    assert place.number_rooms == 5
    assert place.latitude == 45.5
    assert place.longitude == -73.5
    assert place.property_type == "villa"
    assert place.minimum_stay == 2

def test_place_validation():
    """Test Place validation rules! 🎭"""
    from app.models.place import Place
    
    # Test invalid name
    with pytest.raises(ValueError):
        Place(name="", description="Test", owner_id=str(uuid.uuid4()), price_by_night=100.0)
    
    # Test invalid description
    with pytest.raises(ValueError):
        Place(name="Test", description="", owner_id=str(uuid.uuid4()), price_by_night=100.0)
    
    # Test invalid price
    with pytest.raises(ValueError):
        Place(name="Test", description="Test desc", owner_id=str(uuid.uuid4()), price_by_night=-100.0)
    
    # Test invalid status
    with pytest.raises(ValueError):
        Place(
            name="Test",
            description="Test desc",
            owner_id=str(uuid.uuid4()),
            price_by_night=100.0,
            status="invalid"
        )
    
    # Test invalid property type
    with pytest.raises(ValueError):
        Place(
            name="Test",
            description="Test desc",
            owner_id=str(uuid.uuid4()),
            price_by_night=100.0,
            property_type="castle"
        )

def test_place_update(test_place):
    """Test Place update functionality! 🔄"""
    # Update basic attributes
    test_place.update({
        'name': "Updated Manor",
        'price_by_night': 150.0,
        'status': "maintenance"
    })
    
    assert test_place.name == "Updated Manor"
    assert test_place.price_by_night == 150.0
    assert test_place.status == "maintenance"
    
    # Test invalid updates
    with pytest.raises(ValueError):
        test_place.update({'status': 'invalid'})
    
    with pytest.raises(ValueError):
        test_place.update({'price_by_night': -100})

def test_place_to_dict(test_place):
    """Test Place to_dict transformation! 📝"""
    place_dict = test_place.to_dict()
    
    assert isinstance(place_dict, dict)
    assert place_dict['name'] == "Haunted Manor"
    assert place_dict['price_by_night'] == 100.0
    assert 'id' in place_dict
    assert 'created_at' in place_dict
    assert 'updated_at' in place_dict
    assert 'is_active' in place_dict
    assert 'is_deleted' in place_dict

def test_place_get_by_owner(repository):
    """Test Place retrieval by owner! 👻"""
    from app.models.place import Place
    
    owner_id = str(uuid.uuid4())
    
    # Create multiple places
    place1 = Place(
        name="Manor 1",
        description="First haunted house",
        owner_id=owner_id,
        price_by_night=100.0
    )
    place1.save()
    
    place2 = Place(
        name="Manor 2",
        description="Second haunted house",
        owner_id=owner_id,
        price_by_night=150.0
    )
    place2.save()
    
    # Test retrieval
    owner_places = Place.get_by_attr(multiple=True, owner_id=owner_id)
    assert len(owner_places) == 2
    assert all(place.owner_id == owner_id for place in owner_places)

def test_place_get_by_status(repository):
    """Test Place retrieval by status! 🏰"""
    from app.models.place import Place
    
    # Create places with different status
    place1 = Place(
        name="Active Manor",
        description="Available haunted house",
        owner_id=str(uuid.uuid4()),
        price_by_night=100.0,
        status="active"
    )
    place1.save()
    
    place2 = Place(
        name="Maintenance Manor",
        description="Under repair",
        owner_id=str(uuid.uuid4()),
        price_by_night=150.0,
        status="maintenance"
    )
    place2.save()
    
    # Test retrieval
    active_places = Place.get_by_attr(multiple=True, status="active")
    assert all(place.status == "active" for place in active_places)

def test_place_get_by_price_range(repository):
    """Test Place retrieval by price range! 💰"""
    from app.models.place import Place
    
    # Create places with different prices
    place1 = Place(
        name="Budget Manor",
        description="Affordable haunted house",
        owner_id=str(uuid.uuid4()),
        price_by_night=50.0
    )
    place1.save()
    
    place2 = Place(
        name="Luxury Manor",
        description="Expensive haunted house",
        owner_id=str(uuid.uuid4()),
        price_by_night=200.0
    )
    place2.save()
    
    # Test retrieval
    budget_places = Place.get_by_attr(multiple=True, price_by_night=50.0)
    assert len(budget_places) == 1
    assert budget_places[0].name == "Budget Manor"