"""Test module for Place class."""

import unittest, uuid
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review


class TestPlace(unittest.TestCase):
    """Test cases for Place class."""

    def setUp(self):
        # Create unique username (max 18 chars) and email
        unique_id = str(uuid.uuid4())[:6]  # Plus court pour rester dans la limite !
        self.owner = User.create(
            username=f"test_{unique_id}",  # test_ + 6 chars = 11 chars total
            email=f"test_{unique_id}@test.com",
            password="Password123!",
            first_name="Test",
            last_name="Owner"
        )
        
        # Données de test pour Place
        self.test_data = {
            'name': 'Test Place',
            'description': 'A lovely test place',
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': self.owner.id,
            'city': 'Paris',
            'country': 'France',
            'is_available': True,
            'status': 'active',
            'minimum_stay': 2,
            'property_type': 'apartment'
        }
        
        self.place = Place.create(**self.test_data)
        
        self.place = Place.create(**self.test_data)

    def test_initialization(self):
        """Test Place initialization."""
        self.assertEqual(self.place.name, 'Test Place')
        self.assertEqual(self.place.number_rooms, 2)
        self.assertEqual(self.place.price_by_night, 100.0)
        self.assertEqual(self.place.owner_id, self.owner.id)
        self.assertTrue(self.place.is_available)
        self.assertEqual(self.place.status, 'active')
        
        # Test validation errors
        with self.assertRaises(ValueError):
            Place.create(**{**self.test_data, 'number_rooms': -1})
        with self.assertRaises(ValueError):
            Place.create(**{**self.test_data, 'latitude': 91})

    def test_search_and_filters(self):
        """Test search and filter methods."""
        # Test search
        results = Place.search(
            is_available=True,
            property_type='apartment'
        )
        self.assertIn(self.place, results)
        
        # Test price filter
        price_results = Place.filter_by_price(50, 150)
        self.assertIn(self.place, price_results)
        
        # Test capacity filter
        capacity_results = Place.filter_by_capacity(3)
        self.assertIn(self.place, capacity_results)
        
        # Test location search
        location_results = Place.get_by_location(48.8566, 2.3522, 1)
        self.assertIn(self.place, location_results)

    def test_amenities(self):
        """Test amenity-related methods."""
        # Create test amenity
        amenity = Amenity.create(name="WiFi")
        
        # Test add amenity
        self.place.add_amenity(amenity)
        amenities = self.place.get_amenities()
        self.assertIn(amenity, amenities)
        
        # Test remove amenity
        self.place.remove_amenity(amenity)
        amenities = self.place.get_amenities()
        self.assertNotIn(amenity, amenities)

    def test_update(self):
        """Test update method."""
        update_data = {
            'name': 'Updated Place',
            'price_by_night': 150.0,
            'status': 'maintenance'
        }
        
        updated_place = self.place.update(update_data)
        self.assertEqual(updated_place.name, 'Updated Place')
        self.assertEqual(updated_place.price_by_night, 150.0)
        self.assertEqual(updated_place.status, 'maintenance')
        
        # Test invalid updates
        with self.assertRaises(ValueError):
            self.place.update({'owner_id': 'new_id'})
        with self.assertRaises(ValueError):
            self.place.update({'status': 'invalid_status'})

    def test_serialization(self):
        """Test serialization methods."""
        place_dict = self.place.to_dict()
        
        # Check all attributes are present
        expected_attrs = [
            'id', 'name', 'description', 'number_rooms',
            'price_by_night', 'latitude', 'longitude',
            'owner_id', 'is_available', 'status',
            'property_type', 'amenity_ids', 'review_ids'
        ]
        
        for attr in expected_attrs:
            self.assertIn(attr, place_dict)
        
        # Check types
        self.assertIsInstance(place_dict['created_at'], str)
        self.assertIsInstance(place_dict['amenity_ids'], list)

    def tearDown(self):
        """Clean up after tests."""
        # Clear repositories
        Place.repository._storage.clear()
        User.repository._storage.clear()
        Amenity.repository._storage.clear()
        Review.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()