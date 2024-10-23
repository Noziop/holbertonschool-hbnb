"""Test module for Amenity class."""
import unittest
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class."""

    def setUp(self):
        """Set up test cases."""
        self.test_data = {'name': 'WiFi'}
        self.amenity = Amenity.create(**self.test_data)

    def test_initialization(self):
        """Test Amenity initialization."""
        self.assertEqual(self.amenity.name, 'WiFi')
        
        # Test validation errors
        with self.assertRaises(ValueError):
            Amenity.create(name='')
        with self.assertRaises(ValueError):
            Amenity.create(name='Invalid@Name')
        with self.assertRaises(ValueError):
            Amenity.create()  # Missing name

    def test_uniqueness(self):
        """Test name uniqueness."""
        # Try to create amenity with same name
        with self.assertRaises(ValueError):
            Amenity.create(name='WiFi')

    def test_search(self):
        """Test search functionality."""
        # Create additional amenities
        Amenity.create(name='Pool')
        Amenity.create(name='Parking')
        
        # Test search by exact match
        results = Amenity.search(name='Pool')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Pool')
        
        # Test search with no criteria
        all_results = Amenity.search()
        self.assertEqual(len(all_results), 3)

    def test_update(self):
        """Test update functionality."""
        # Test valid update
        self.amenity.update({'name': 'High-Speed WiFi'})
        self.assertEqual(self.amenity.name, 'High-Speed WiFi')
        
        # Test invalid updates
        with self.assertRaises(ValueError):
            self.amenity.update({'name': ''})
        with self.assertRaises(ValueError):
            self.amenity.update({'name': 'Invalid@Name'})

        # Test duplicate name
        other = Amenity.create(name='Pool')
        with self.assertRaises(ValueError):
            other.update({'name': 'High-Speed WiFi'})

    def test_places_relationship(self):
        """Test relationship with places."""
        # Create a test place
        from app.models.user import User
        owner = User.create(
            username="testuser",
            email="test@test.com",
            password="Password123!",
            first_name="Test",
            last_name="User"
        )
        
        place = Place.create(
            name="Test Place",
            description="Test Description",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=2,
            price_by_night=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )
        
        # Add amenity to place
        place.add_amenity(self.amenity)
        
        # Test get_places
        places = self.amenity.get_places()
        self.assertIn(place, places)
        
        # Test removal
        place.remove_amenity(self.amenity)
        places = self.amenity.get_places()
        self.assertNotIn(place, places)

    def test_serialization(self):
        """Test serialization."""
        amenity_dict = self.amenity.to_dict()
        
        # Check required attributes
        self.assertIn('id', amenity_dict)
        self.assertIn('name', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        
        # Check values
        self.assertEqual(amenity_dict['name'], 'WiFi')

    def tearDown(self):
        """Clean up after tests."""
        Amenity.repository._storage.clear()
        Place.repository._storage.clear()
        PlaceAmenity.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()