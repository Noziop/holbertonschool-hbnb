import unittest
import uuid
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.placeamenity import PlaceAmenity
from app.persistence.repository import InMemoryRepository

class TestPlaceAmenityFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()
        self.user = self.facade.create_user({
            'username': f'testuser_{uuid.uuid4().hex[:8]}',  # Generate a unique username
            'email': f'test_{uuid.uuid4().hex[:8]}@example.com',
            'password': 'password123'
        })
        self.place = self.facade.create_place({
            'name': 'Test Place',
            'description': 'A test place',
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100,
            'latitude': 45.5,
            'longitude': -73.5,
            'owner_id': self.user.id
        })
        self.amenity = self.facade.create_amenity({'name': 'Wi-Fi'})

    def tearDown(self):
        Place.repository = InMemoryRepository()
        Amenity.repository = InMemoryRepository()
        PlaceAmenity.repository = InMemoryRepository()

    def test_add_amenity_to_place_valid(self):
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertIn(self.amenity, place_amenities)

    def test_add_amenity_to_place_nonexistent_place(self):
        with self.assertRaises(ValueError):
            self.facade.add_amenity_to_place('nonexistent_place_id', self.amenity.id)

    def test_add_amenity_to_place_nonexistent_amenity(self):
        with self.assertRaises(ValueError):
            self.facade.add_amenity_to_place(self.place.id, 'nonexistent_amenity_id')

    def test_add_amenity_to_place_duplicate(self):
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        # Adding the same amenity again should not raise an error
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertEqual(len(place_amenities), 1)

    def test_remove_amenity_from_place_valid(self):
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        self.facade.remove_amenity_from_place(self.place.id, self.amenity.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertNotIn(self.amenity, place_amenities)

    def test_remove_amenity_from_place_nonexistent_association(self):
        with self.assertRaises(ValueError):
            self.facade.remove_amenity_from_place(self.place.id, self.amenity.id)

    def test_get_amenities_for_place_valid(self):
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertEqual(len(place_amenities), 1)
        self.assertEqual(place_amenities[0].id, self.amenity.id)

    def test_get_amenities_for_place_empty(self):
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertEqual(len(place_amenities), 0)

    def test_get_places_with_amenity_valid(self):
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        places = self.facade.get_places_with_amenity(self.amenity.id)
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0].id, self.place.id)

    def test_get_places_with_amenity_empty(self):
        places = self.facade.get_places_with_amenity(self.amenity.id)
        self.assertEqual(len(places), 0)

    def test_add_multiple_amenities_to_place(self):
        amenity2 = self.facade.create_amenity({'name': 'Pool'})
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        self.facade.add_amenity_to_place(self.place.id, amenity2.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertEqual(len(place_amenities), 2)

    def test_add_amenity_to_multiple_places(self):
        place2 = self.facade.create_place({
            'name': 'Another Place',
            'description': 'Another test place',
            'number_rooms': 1,
            'number_bathrooms': 1,
            'max_guest': 2,
            'price_by_night': 50,
            'latitude': 46.5,
            'longitude': -74.5,
            'owner_id': self.user.id
        })
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        self.facade.add_amenity_to_place(place2.id, self.amenity.id)
        places = self.facade.get_places_with_amenity(self.amenity.id)
        self.assertEqual(len(places), 2)

    def test_remove_all_amenities_from_place(self):
        amenity2 = self.facade.create_amenity({'name': 'Pool'})
        self.facade.add_amenity_to_place(self.place.id, self.amenity.id)
        self.facade.add_amenity_to_place(self.place.id, amenity2.id)
        self.facade.remove_amenity_from_place(self.place.id, self.amenity.id)
        self.facade.remove_amenity_from_place(self.place.id, amenity2.id)
        place_amenities = self.facade.get_amenities_for_place(self.place.id)
        self.assertEqual(len(place_amenities), 0)

    def test_add_amenity_to_place_with_invalid_ids(self):
        with self.assertRaises(ValueError):
            self.facade.add_amenity_to_place('', self.amenity.id)
        with self.assertRaises(ValueError):
            self.facade.add_amenity_to_place(self.place.id, '')
        with self.assertRaises(ValueError):
            self.facade.add_amenity_to_place('', '')

    def test_get_amenities_for_nonexistent_place(self):
        with self.assertRaises(ValueError):
            self.facade.get_amenities_for_place('nonexistent_place_id')

    def test_get_places_with_nonexistent_amenity(self):
        places = self.facade.get_places_with_amenity('nonexistent_amenity_id')
        self.assertEqual(len(places), 0)

if __name__ == '__main__':
    unittest.main()