"""Test module for Amenity class. Rating supernatural features since 1888! 👻"""
import unittest
import uuid
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.placeamenity import PlaceAmenity


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class. Where haunted features come to life! 🏚️"""

    def setUp(self):
        """Prepare our supernatural testing grounds! 🌙"""
        unique_id = str(uuid.uuid4())[:6]
        self.test_data = {'name': f'WiFi_{unique_id}'}
        self.amenity = Amenity.create(**self.test_data)

    def test_initialization(self):
        """Test Amenity initialization. Birth of a supernatural feature! ✨"""
        self.assertEqual(self.amenity.name, self.test_data['name'])
        
        # Test when the spirits reject invalid data
        with self.assertRaises(ValueError):
            Amenity.create(name='')  # Empty names anger the spirits!
        with self.assertRaises(ValueError):
            Amenity.create(name='Invalid@Name')  # Cursed characters!
        with self.assertRaises(ValueError):
            Amenity.create(**{})  # Empty offerings are rejected!

    def test_uniqueness(self):
        """Test name uniqueness. Each spirit must be unique! 👻"""
        # Try to create a doppelganger amenity
        with self.assertRaises(ValueError):
            Amenity.create(name=self.test_data['name'])

    def test_search(self):
        """Test search functionality. Ghost hunting for features! 🔍"""
        unique_id = str(uuid.uuid4())[:6]
        # Create additional spectral amenities
        Amenity.create(name=f'Pool_{unique_id}')
        Amenity.create(name=f'Parking_{unique_id}')
        
        # Test search by exact match
        results = Amenity.get_by_attr(name=f'Pool_{unique_id}')
        self.assertIsNotNone(results)
        self.assertEqual(results.name, f'Pool_{unique_id}')

    def test_update(self):
        """Test update functionality. Even ghosts need upgrades! 🔄"""
        new_name = f'High-Speed-WiFi_{str(uuid.uuid4())[:6]}'
        # Test valid update
        self.amenity.update({'name': new_name})
        self.assertEqual(self.amenity.name, new_name)
        
        # Test when the spirits reject changes
        with self.assertRaises(ValueError):
            self.amenity.update({'name': ''})
        with self.assertRaises(ValueError):
            self.amenity.update({'name': 'Invalid@Name'})

    def test_places_relationship(self):
        """Test relationship with places. Haunting multiple locations! 👻"""
        unique_id = str(uuid.uuid4())[:6]
        # Create a test ghost owner
        from app.models.user import User
        owner = User.create(
            username=f"Ghost_{unique_id}",
            email=f"ghost_{unique_id}@haunted.com",
            password="Haunted123!",
            first_name="Spooky",
            last_name="Owner"
        )
        
        # Create a haunted place
        place = Place.create(
            name="Haunted Manor",
            description="Where spirits come to rest",
            number_rooms=13,
            number_bathrooms=4,
            max_guest=666,
            price_by_night=99.99,
            latitude=13.13,
            longitude=66.6,
            owner_id=owner.id
        )
        
        # Bind the supernatural feature to the place
        place.add_amenity(self.amenity)
        
        # Test if the haunting was successful
        places = self.amenity.get_places()
        self.assertIn(place, places)
        
        # Test exorcism
        place.remove_amenity(self.amenity)
        places = self.amenity.get_places()
        self.assertNotIn(place, places)

    def test_serialization(self):
        """Test serialization. Converting supernatural to mortal format! 📜"""
        amenity_dict = self.amenity.to_dict()
        
        # Check if all spectral attributes are present
        self.assertIn('id', amenity_dict)
        self.assertIn('name', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        
        # Verify the essence remains unchanged
        self.assertEqual(amenity_dict['name'], self.test_data['name'])

    def tearDown(self):
        """Clean up our supernatural mess! 🧹"""
        Amenity.repository._storage.clear()
        Place.repository._storage.clear()
        PlaceAmenity.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()