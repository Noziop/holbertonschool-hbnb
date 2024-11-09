# app/tests/test_spooky/test_models/test_place.py
"""Test module for our Place model! 👻"""
import pytest
from datetime import datetime, timezone
import uuid

@pytest.fixture(autouse=True)
def setup_repository():
    """Setup clean repository for each test! 🏰"""
    from app.models.place import Place
    from app.models.user import User
    from app.persistence.repository import InMemoryRepository
    
    # Create new repositories and clear any existing data
    repo = InMemoryRepository()
    repo._storage.clear()
    
    # Set repositories for both Place and User
    Place.repository = repo
    User.repository = repo
    
    yield repo
    
    # Cleanup after test
    repo._storage.clear()

@pytest.fixture
def test_owner():
    """Create a test owner for places! 👻"""
    from app.models.user import User
    
    owner = User(
        username="ghost_owner",
        email="owner@haunted.com",
        password="Ghost123!@#",
        first_name="Ghost",
        last_name="Owner"
    )
    owner.save()
    return owner

@pytest.fixture
def test_place(test_owner):
    """Create a test place! 🏰"""
    from app.models.place import Place
    
    place = Place(
        name="Haunted Manor",
        description="A spooky place with lots of ghosts!",
        owner_id=test_owner.id,  # Utiliser un vrai owner_id
        price_by_night=100.0,
        number_rooms=3,
        number_bathrooms=2,
        max_guest=6,
        city="Ghostville",
        country="Spookyland"
    )
    place.save()
    return place

def test_place_creation(test_owner):
    """Test basic Place creation with default values! 🎭"""
    from app.models.place import Place
    
    place = Place(
        name="Haunted Manor",
        description="A spooky place with lots of ghosts!",
        owner_id=test_owner.id,  # Utiliser un vrai owner_id
        price_by_night=100.0
    )
    
    # Required attributes
    assert place.name == "Haunted Manor"
    assert place.description == "A spooky place with lots of ghosts!"
    assert place.owner_id == test_owner.id
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

def test_place_with_all_attributes(test_owner):
    """Test Place creation with all attributes! 🏰"""
    from app.models.place import Place
    
    place = Place(
        name="Luxury Ghost Manor",
        description="The most haunted mansion in town!",
        owner_id=test_owner.id,  # Utiliser un vrai owner_id
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

def test_place_validation(test_owner):
    """Test Place validation rules! 🎭"""
    from app.models.place import Place
    
    # Test invalid name
    with pytest.raises(ValueError):
        Place(name="", description="Test", owner_id=test_owner.id, price_by_night=100.0)
    
    # Test invalid description
    with pytest.raises(ValueError):
        Place(name="Test", description="", owner_id=test_owner.id, price_by_night=100.0)
    
    # Test invalid price
    with pytest.raises(ValueError):
        Place(name="Test", description="Test desc", owner_id=test_owner.id, price_by_night=-100.0)
    
    # Test invalid status
    with pytest.raises(ValueError):
        Place(
            name="Test",
            description="Test desc",
            owner_id=test_owner.id,
            price_by_night=100.0,
            status="invalid"
        )
    
    # Test invalid property type
    with pytest.raises(ValueError):
        Place(
            name="Test",
            description="Test desc",
            owner_id=test_owner.id,
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
    assert place_dict['owner_id'] == test_place.owner_id
    assert 'id' in place_dict
    assert 'created_at' in place_dict
    assert 'updated_at' in place_dict
    assert 'is_active' in place_dict
    assert 'is_deleted' in place_dict

def test_place_get_by_owner(test_owner):
    """Test Place retrieval by owner! 👻"""
    from app.models.place import Place
    
    # Create multiple places
    place1 = Place(
        name="Manor 1",
        description="First haunted house",
        owner_id=test_owner.id,
        price_by_night=100.0
    )
    place1.save()
    
    place2 = Place(
        name="Manor 2",
        description="Second haunted house",
        owner_id=test_owner.id,
        price_by_night=150.0
    )
    place2.save()
    
    # Test retrieval
    owner_places = Place.get_by_attr(multiple=True, owner_id=test_owner.id)
    assert len(owner_places) == 2
    assert all(place.owner_id == test_owner.id for place in owner_places)

def test_place_get_by_status(test_owner):
    """Test Place retrieval by status! 🏰"""
    from app.models.place import Place
    
    # Create places with different status
    place1 = Place(
        name="Active Manor",
        description="Available haunted house",
        owner_id=test_owner.id,
        price_by_night=100.0,
        status="active"
    )
    place1.save()
    
    place2 = Place(
        name="Maintenance Manor",
        description="Under repair",
        owner_id=test_owner.id,
        price_by_night=150.0,
        status="maintenance"
    )
    place2.save()
    
    # Test retrieval
    maintenance_places = Place.get_by_attr(multiple=True, status="maintenance")
    assert len(maintenance_places) == 1
    assert all(place.status == "maintenance" for place in maintenance_places)

def test_place_get_by_price_range(test_owner):
    """Test Place retrieval by price range! 💰"""
    from app.models.place import Place
    
    # Create places with different prices
    place1 = Place(
        name="Budget Manor",
        description="Affordable haunted house",
        owner_id=test_owner.id,
        price_by_night=50.0
    )
    place1.save()
    
    place2 = Place(
        name="Luxury Manor",
        description="Expensive haunted house",
        owner_id=test_owner.id,
        price_by_night=200.0
    )
    place2.save()
    
    # Test retrieval
    budget_places = Place.get_by_attr(multiple=True, price_by_night=50.0)
    assert len(budget_places) == 1
    assert budget_places[0].name == "Budget Manor"

def test_place_validation_edge_cases(test_owner):
    """Test Place validation edge cases! 🏰"""
    from app.models.place import Place
    
    # Test latitude validation
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            latitude=91.0  # Invalid latitude
        )
    
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            latitude=-91.0  # Invalid latitude
        )
    
    # Test longitude validation
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            longitude=181.0  # Invalid longitude
        )
    
    # Test status validation
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            status="invalid_status"
        )

    def test_place_search_methods(test_owner):
        """Test Place search methods! 🔍"""
        from app.models.place import Place
        
        # Create test places
        place1 = Place(
            name="Budget Manor",
            description="Affordable haunted house",
            owner_id=test_owner.id,
            price_by_night=50.0,
            city="Ghostville",
            max_guest=2
        )
        place1.save()
        
        place2 = Place(
            name="Luxury Manor",
            description="Expensive haunted mansion",
            owner_id=test_owner.id,
            price_by_night=200.0,
            city="Spooktown",
            max_guest=10
        )
        place2.save()
        
        # Test filter_by_price
        budget_places = Place.filter_by_price(0, 100)
        assert len(budget_places) == 1
        assert budget_places[0].name == "Budget Manor"
        
        # Test filter_by_capacity
        large_places = Place.filter_by_capacity(5)
        assert len(large_places) == 1
        assert large_places[0].name == "Luxury Manor"
        
        small_places = Place.filter_by_capacity(2)
        assert len(small_places) == 2

def test_place_amenity_management(test_owner):
    """Test Place amenity management! ✨"""
    from app.models.place import Place
    from app.models.amenity import Amenity
    
    # Create test place
    place = Place(
        name="Haunted Manor",
        description="A very spooky place!",
        owner_id=test_owner.id,
        price_by_night=100.0
    )
    place.save()
    
    # Create test amenity
    amenity = Amenity(
        name="Ghost Detector",
        description="Detects supernatural activity!"
    )
    amenity.save()
    
    # Test add_amenity
    place.add_amenity(amenity)
    
    # Test get_amenities
    amenities = place.get_amenities()
    assert len(amenities) == 1
    assert amenities[0].name == "Ghost Detector"
    
    # Test remove_amenity
    place.remove_amenity(amenity)
    amenities = place.get_amenities()
    assert len(amenities) == 0

def test_place_edge_cases(test_owner):
    """Test Place edge cases! 🏰"""
    from app.models.place import Place
    
    # Test latitude/longitude validation
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            latitude=91.0  # Invalid
        )
    
    # Test location-based search
    place1 = Place(
        name="Located Manor",
        description="Test Description",
        owner_id=test_owner.id,
        price_by_night=100.0,
        latitude=45.5,
        longitude=-73.5
    )
    place1.save()
    
    place2 = Place(
        name="Far Manor",
        description="Test Description",
        owner_id=test_owner.id,
        price_by_night=100.0,
        latitude=48.5,  # ~300km away
        longitude=-73.5
    )
    place2.save()
    
    # Test get_by_location
    nearby = Place.get_by_location(45.5, -73.5, 10.0)  # 10km radius
    assert len(nearby) == 1
    assert nearby[0].name == "Located Manor"
    
    # Test larger radius
    all_places = Place.get_by_location(45.5, -73.5, 500.0)  # 500km radius
    assert len(all_places) == 2

def test_place_validation_edge_cases(test_owner):
    """Test Place validation edge cases! 🏰"""
    from app.models.place import Place
    
    # Test latitude/longitude type errors
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            latitude="not a float"  # Test type error
        )
    
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            longitude="not a float"  # Test type error
        )
    
    # Test price type error
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night="not a number"  # Test type error
        )
    
    # Test positive integer validation errors
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            number_rooms="not a number"  # Test type error
        )

def test_place_amenity_errors(test_owner):
    """Test Place amenity error handling! 🎭"""
    from app.models.place import Place
    from app.models.amenity import Amenity
    
    # Create test place
    place = Place(
        name="Test Manor",
        description="Test Description",
        owner_id=test_owner.id,
        price_by_night=100.0
    )
    place.save()
    
    # Test add_amenity with invalid amenity
    invalid_amenity = Amenity(name="Invalid", description="Test")  # Non sauvegardé
    with pytest.raises(Exception):
        place.add_amenity(invalid_amenity)
    
    # Test remove_amenity with non-existent link
    amenity = Amenity(name="Test", description="Test")
    amenity.save()
    with pytest.raises(Exception):
        place.remove_amenity(amenity)  # Pas de lien existant

def test_place_coordinates_validation(test_owner):
    """Test Place coordinates validation! 🗺️"""
    from app.models.place import Place
    
    # Test invalid latitude type
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            latitude="not a number"  # Test type error
        )
    
    # Test invalid longitude type
    with pytest.raises(ValueError):
        Place(
            name="Test Manor",
            description="Test Description",
            owner_id=test_owner.id,
            price_by_night=100.0,
            longitude="not a number"  # Test type error
        )

def test_place_amenities_errors(test_owner):
    """Test Place amenities error handling! 🎭"""
    from app.models.place import Place
    import sys
    
    # Create place
    place = Place(
        name="Test Manor",
        description="Test Description",
        owner_id=test_owner.id,
        price_by_night=100.0
    )
    place.save()
    
    # Test get_amenities with missing module
    old_module = sys.modules.get('app.models.placeamenity')
    sys.modules['app.models.placeamenity'] = None
    
    try:
        with pytest.raises(Exception):
            place.get_amenities()
    finally:
        sys.modules['app.models.placeamenity'] = old_module

