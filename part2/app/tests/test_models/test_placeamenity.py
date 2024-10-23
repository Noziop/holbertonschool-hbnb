"""Test module for PlaceAmenity. Where places and amenities find their soulmates! 👻💘"""
import unittest
import uuid
from datetime import datetime
from app.models.placeamenity import PlaceAmenity
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User


class TestPlaceAmenity(unittest.TestCase):
    """Test cases for PlaceAmenity. Matchmaking in the spirit world! 🏚️"""

    def setUp(self):
        """Set up our haunted test scene! 🌙"""
        unique_id = str(uuid.uuid4())[:6]
        
        # Summon our test user
        self.user = User.create(
            username=f"Ghost_{unique_id}",
            email=f"ghost_{unique_id}@haunted.com",
            password="Haunted123!",
            first_name="Spooky",
            last_name="Owner"
        )
        
        # Create our haunted place
        self.place = Place.create(
            name="Haunted Manor",
            description="Where spirits come to rest",
            number_rooms=13,
            number_bathrooms=4,
            max_guest=666,
            price_by_night=99.99,
            latitude=13.13,
            longitude=66.6,
            owner_id=self.user.id
        )
        
        # Create our supernatural amenity
        self.amenity = Amenity.create(
            name=f"Ghostly_{unique_id}",
            description="For the discerning spirit"
        )
        
        # Our haunted connection data
        self.test_data = {
            'place_id': self.place.id,
            'amenity_id': self.amenity.id
        }
        
        # Create the supernatural bond
        self.pa = PlaceAmenity.create(**self.test_data)

    def test_create(self):
        """Test creation of a haunted connection! 👻"""
        self.assertIsInstance(self.pa, PlaceAmenity)
        self.assertEqual(self.pa.place_id, self.place.id)
        self.assertEqual(self.pa.amenity_id, self.amenity.id)

    def test_get_by_place(self):
        """Test finding amenities haunting a place! 🏚️"""
        results = PlaceAmenity.get_by_attr(multiple=True, place_id=self.place.id)
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.pa.id)

    def test_get_by_amenity(self):
        """Test finding places blessed with an amenity! ✨"""
        results = PlaceAmenity.get_by_attr(multiple=True, amenity_id=self.amenity.id)
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.pa.id)

    def test_update(self):
        """Test updating a supernatural connection! 🔮"""
        new_amenity = Amenity.create(
            name=f"NewSpirit_{str(uuid.uuid4())[:6]}",
            description="A fresh haunting"
        )
        self.pa.update({'amenity_id': new_amenity.id})
        self.assertEqual(self.pa.amenity_id, new_amenity.id)

    def test_delete_by_place_and_amenity(self):
        """Test breaking the supernatural bond! ⚡"""
        self.assertTrue(
            PlaceAmenity.delete_by_place_and_amenity(
                self.place.id, 
                self.amenity.id
            )
        )
        results = PlaceAmenity.get_by_attr(multiple=True, place_id=self.place.id)
        self.assertEqual(len(results), 0)

    def test_to_dict(self):
        """Test converting our haunted bond to mortal-readable format! 📜"""
        pa_dict = self.pa.to_dict()
        self.assertEqual(pa_dict['place_id'], self.place.id)
        self.assertEqual(pa_dict['amenity_id'], self.amenity.id)

    def tearDown(self):
        """Clean up after our supernatural experiments! 🧹"""
        PlaceAmenity.repository._storage.clear()
        Place.repository._storage.clear()
        Amenity.repository._storage.clear()
        User.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()