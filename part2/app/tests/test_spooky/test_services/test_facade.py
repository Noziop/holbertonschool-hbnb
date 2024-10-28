# app/tests/test_spooky/test_services/test_facade.py

import pytest
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.placeamenity import PlaceAmenity

@pytest.fixture
def facade():
    """Create a haunted facade! 🏰"""
    return HBnBFacade()

@pytest.fixture
def test_user_data():
    """Create test user data! 👻"""
    return {
        "username": "ghost_user",
        "email": "ghost@haunted.com",
        "password": "Boo123!@#",
        "first_name": "Ghost",
        "last_name": "User"
    }

@pytest.fixture
def test_user(facade, test_user_data):
    """Create a test user! 👻"""
    user = facade.create(User, test_user_data)
    return user

@pytest.fixture
def test_place_data(test_user):
    """Create test place data! 🏰"""
    return {
        "name": "Haunted Manor",
        "description": "A very spooky place!",
        "owner_id": test_user.id,
        "price_by_night": 100.0
    }

@pytest.fixture(autouse=True)
def clean_repository():
    """Clean repository before each test! 🧹"""
    from app.persistence.repository import InMemoryRepository
    from app.models.user import User
    from app.models.place import Place
    from app.models.amenity import Amenity
    from app.models.review import Review
    from app.models.placeamenity import PlaceAmenity
    
    # Create new repository
    repo = InMemoryRepository()
    repo._storage.clear()
    
    # Assign to all models
    User.repository = repo
    Place.repository = repo
    Amenity.repository = repo
    Review.repository = repo
    PlaceAmenity.repository = repo
    
    yield repo
    
    # Clean after test
    repo._storage.clear()

def test_create_entity(facade, test_user_data):
    """Test entity creation! ✨"""
    user = facade.create(User, test_user_data)
    assert isinstance(user, User)
    assert user.username == test_user_data["username"]

def test_get_entity(facade, test_user_data):
    """Test entity retrieval! 🔍"""
    user = facade.create(User, test_user_data)
    retrieved = facade.get(User, user.id)
    assert retrieved.id == user.id

def test_update_entity(facade, test_user_data):
    """Test entity update! 🌟"""
    user = facade.create(User, test_user_data)
    updated = facade.update(User, user.id, {"first_name": "Updated"})
    assert updated.first_name == "Updated"

def test_delete_entity(facade, test_user_data):
    """Test entity deletion! ⚡"""
    user = facade.create(User, test_user_data)
    result = facade.delete(User, user.id)
    assert result is True
    
    # Verify soft deletion
    deleted_user = facade.get(User, user.id)
    assert deleted_user.is_deleted is True
    assert deleted_user.is_active is False

def test_place_amenity_link(facade, test_place_data):
    """Test place-amenity linking! 🔗"""
    # Create place and amenity
    place = facade.create(Place, test_place_data)
    amenity = facade.create(Amenity, {
        "name": "Ghost Detector",
        "description": "Detects supernatural activity!"
    })

    # Create link
    link = facade.link_place_amenity(place.id, amenity.id)
    assert link.place_id == place.id
    assert link.amenity_id == amenity.id

def test_facade_error_handling(facade):
    """Test facade error handling! 🎭"""
    # Test get with invalid ID
    with pytest.raises(ValueError):  # Plus spécifique que Exception
        facade.get(User, "invalid-id")
    
    # Test update with invalid ID
    with pytest.raises(ValueError):  # Plus spécifique que Exception
        facade.update(User, "invalid-id", {"first_name": "Test"})
    
    # Test find avec critères invalides - pas besoin de tester l'exception
    results = facade.find(User, invalid_field="test")
    assert len(results) == 0  # Vérifie juste que c'est vide

def test_find_entities_complete(facade, test_user_data):
    """Test entity search completely! 🔮"""
    # Create multiple users
    user1 = facade.create(User, test_user_data)
    user2 = facade.create(User, {
        **test_user_data,
        "username": "another_ghost",
        "email": "another@haunted.com"
    })
    
    # Test find with single criterion
    users = facade.find(User, username="ghost_user")
    assert len(users) == 1
    assert users[0].id == user1.id
    
    # Test find with multiple criteria
    users = facade.find(User, is_active=True, is_deleted=False)
    assert len(users) >= 2
    
    # Test find with no results
    empty = facade.find(User, username="nonexistent")
    assert len(empty) == 0

def test_place_amenity_link_complete(facade, test_place_data):
    """Test place-amenity linking completely! 🔗"""
    # Create place and amenity
    place = facade.create(Place, test_place_data)
    amenity = facade.create(Amenity, {
        "name": "Ghost Detector",
        "description": "Detects supernatural activity!"
    })
    
    # Test successful link
    link = facade.link_place_amenity(place.id, amenity.id)
    assert isinstance(link, PlaceAmenity)
    assert link.place_id == place.id
    assert link.amenity_id == amenity.id
    
    # Test duplicate link
    with pytest.raises(ValueError):
        facade.link_place_amenity(place.id, amenity.id)
    
    # Test invalid IDs
    with pytest.raises(Exception):
        facade.link_place_amenity("invalid-id", amenity.id)
    with pytest.raises(Exception):
        facade.link_place_amenity(place.id, "invalid-id")

def test_facade_model_specific_operations():
    """Test model-specific operations through facade"""
    facade = HBnBFacade()
    
    # Test Place specific validations
    with pytest.raises(ValueError):
        facade.create(Place, {
            'name': '',  # Invalid name
            'description': 'Test',
            'owner_id': 'test_id',
            'price_by_night': 100
        })
    
    # Test User specific operations
    user = facade.create(User, {
        'username': 'GhostTester',
        'email': 'test@test.com',
        'password': 'Test123!@#',
        'first_name': 'Ghost',
        'last_name': 'Tester'
    })
    assert user.check_password('Test123!@#')