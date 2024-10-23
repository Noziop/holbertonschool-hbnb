"""Test module for Place class. Welcome to the haunted real estate! 🏚️"""
import unittest
import uuid
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class TestPlace(unittest.TestCase):
    """Test cases for Place class. Rating haunted properties since 1888! 👻"""

    def setUp(self):
        """Prepare our haunted testing grounds! 🏚️"""
        unique_id = str(uuid.uuid4())[:6]
        
        # Create test user
        self.user = User.create(
            username=f"Ghost_{unique_id}",
            email=f"ghost_{unique_id}@haunted.com",
            password="Haunted123!",
            first_name="Test",
            last_name="Owner"
        )
        
        # Our haunted test data
        self.test_data = {
            'name': 'Test Place',
            'description': 'Test Description',
            'number_rooms': 1,
            'number_bathrooms': 1,
            'max_guest': 2,
            'price_by_night': 100.0,
            'latitude': 0.0,
            'longitude': 0.0,
            'owner_id': self.user.id,
            'city': 'Test City',
            'property_type': 'apartment'
        }
        
        # Create our haunted place
        self.place = Place.create(**self.test_data)

    def test_initialization(self):
        """Test Place initialization. Summoning a new haunted property! 👻"""
        self.assertEqual(self.place.name, self.test_data['name'])
        self.assertEqual(self.place.number_rooms, self.test_data['number_rooms'])
        self.assertEqual(self.place.price_by_night, self.test_data['price_by_night'])
        self.assertEqual(self.place.owner_id, self.user.id)
        self.assertTrue(self.place.is_available)
        self.assertEqual(self.place.status, 'active')
        
        # Test when the spirits reject invalid data
        with self.assertRaises(ValueError):
            Place.create(**{**self.test_data, 'number_rooms': -1})
        with self.assertRaises(ValueError):
            Place.create(**{**self.test_data, 'latitude': 91})

    def test_search_and_filters(self):
        """Test search and filters like a ghost hunting for the perfect haunt! 👻"""
        # Test location search
        location_results = Place.get_by_location(
            latitude=0.0,
            longitude=0.0,
            radius=10.0
        )
        self.assertIn(self.place, location_results)

        # Test price filter
        price_results = Place.filter_by_price(
            min_price=50.0,
            max_price=150.0
        )
        self.assertIn(self.place, price_results)

        # Test capacity filter
        capacity_results = Place.filter_by_capacity(min_guests=2)
        self.assertIn(self.place, capacity_results)

    def test_amenities(self):
        """Test amenity-related methods. Every haunted house needs its features! 👻"""
        # Create a spectral amenity
        amenity = Amenity.create(
            name=f"Ghostly_WiFi_{str(uuid.uuid4())[:6]}",
            description="For the modern ghost"
        )
        
        # Test adding supernatural features
        self.place.add_amenity(amenity)
        amenities = self.place.get_amenities()
        self.assertIn(amenity, amenities)
        
        # Test exorcising features
        self.place.remove_amenity(amenity)
        amenities = self.place.get_amenities()
        self.assertNotIn(amenity, amenities)

    def test_update(self):
        """Test update method. Even haunted houses need renovations! 🏚️"""
        update_data = {
            'name': 'Updated Place',
            'price_by_night': 150.0,
            'status': 'maintenance'
        }
        
        updated_place = self.place.update(update_data)
        self.assertEqual(updated_place.name, 'Updated Place')
        self.assertEqual(updated_place.price_by_night, 150.0)
        self.assertEqual(updated_place.status, 'maintenance')
        
        # Test when the spirits reject changes
        with self.assertRaises(ValueError):
            self.place.update({'owner_id': 'new_id'})
        with self.assertRaises(ValueError):
            self.place.update({'status': 'invalid_status'})

    def test_serialization(self):
        """Test serialization. Converting haunted properties to mortal format! 📜"""
        place_dict = self.place.to_dict()
        
        # Check all spectral attributes are present
        expected_attrs = [
            'id', 'name', 'description', 'number_rooms',
            'price_by_night', 'latitude', 'longitude',
            'owner_id', 'is_available', 'status',
            'property_type', 'amenity_ids', 'review_ids'
        ]
        
        for attr in expected_attrs:
            self.assertIn(attr, place_dict)
        
        # Check the types are properly materialized
        self.assertIsInstance(place_dict['created_at'], str)
        self.assertIsInstance(place_dict['amenity_ids'], list)

    def tearDown(self):
        """Clean up our haunted test environment! 🧹"""
        Place.repository._storage.clear()
        User.repository._storage.clear()
        Amenity.repository._storage.clear()
        Review.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()