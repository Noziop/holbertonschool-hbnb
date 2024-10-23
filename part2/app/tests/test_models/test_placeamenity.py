"""Test module for PlaceAmenity. Let's match and test! 💘"""
import unittest
from datetime import datetime
from app.models.placeamenity import PlaceAmenity
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User


class TestPlaceAmenity(unittest.TestCase):
    def setUp(self):
        # Create test user
        self.user = User.create(
            username="TestOwner",
            email="owner@test.com",
            password="Password123!",
            first_name="Test",
            last_name="Owner"
        )
        
        # Create test place
        self.place = Place.create(
            name="Test Place",
            description="Test Description",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=2,
            price_by_night=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=self.user.id
        )
        
        # Create test amenity
        self.amenity = Amenity.create(
            name="Test Amenity",
            description="Test Description"
        )
        
        # Test data
        self.test_data = {
            'place_id': self.place.id,
            'amenity_id': self.amenity.id
        }
        
        self.pa = PlaceAmenity.create(**self.test_data)

    def test_create(self):
        self.assertIsInstance(self.pa, PlaceAmenity)
        self.assertEqual(self.pa.place_id, self.place.id)
        self.assertEqual(self.pa.amenity_id, self.amenity.id)

    def test_get_by_place(self):
        results = PlaceAmenity.get_by_place(self.place.id)
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.pa.id)

    def test_get_by_amenity(self):
        results = PlaceAmenity.get_by_amenity(self.amenity.id)
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.pa.id)

    def test_update(self):
        new_amenity = Amenity.create(
            name="New Amenity",
            description="New Description"
        )
        self.pa.update({'amenity_id': new_amenity.id})
        self.assertEqual(self.pa.amenity_id, new_amenity.id)

    def test_delete_by_place_and_amenity(self):
        self.assertTrue(
            PlaceAmenity.delete_by_place_and_amenity(
                self.place.id, 
                self.amenity.id
            )
        )
        results = PlaceAmenity.get_by_place(self.place.id)
        self.assertEqual(len(results), 0)

    def test_to_dict(self):
        pa_dict = self.pa.to_dict()
        self.assertEqual(pa_dict['place_id'], self.place.id)
        self.assertEqual(pa_dict['amenity_id'], self.amenity.id)

    def tearDown(self):
        PlaceAmenity.repository._storage.clear()
        Place.repository._storage.clear()
        Amenity.repository._storage.clear()
        User.repository._storage.clear()