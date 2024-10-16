import unittest
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestPlaceFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()
        self.user = User.create(username="testuser", email="test@example.com", password="password123")
        self.place_data = {
            'name': 'Cozy Cottage',
            'description': 'A beautiful cottage in the countryside',
            'number_rooms': 3,
            'number_bathrooms': 2,
            'max_guest': 5,
            'price_by_night': 100.50,
            'latitude': 45.5,
            'longitude': -73.5,
            'owner_id': self.user.id,
            'city': 'Montreal',
            'country': 'Canada'
        }

    def tearDown(self):
        Place.repository = InMemoryRepository()
        User.repository = InMemoryRepository()
        Amenity.repository = InMemoryRepository()

    def test_create_place_valid(self):
        place = self.facade.create_place(self.place_data)
        self.assertIsInstance(place, Place)
        self.assertEqual(place.name, 'Cozy Cottage')
        self.assertEqual(place.owner_id, self.user.id)

    def test_create_place_invalid_data(self):
        invalid_data = self.place_data.copy()
        invalid_data['max_guest'] = 'invalid'
        with self.assertRaises(ValueError):
            self.facade.create_place(invalid_data)

    def test_get_place_existing(self):
        created_place = self.facade.create_place(self.place_data)
        retrieved_place = self.facade.get_place(created_place.id)
        self.assertEqual(created_place.id, retrieved_place.id)
        self.assertEqual(retrieved_place.name, 'Cozy Cottage')

    def test_get_place_nonexistent(self):
        with self.assertRaises(ValueError):
            self.facade.get_place('nonexistent_id')

    def test_update_place_valid(self):
        place = self.facade.create_place(self.place_data)
        updated_data = {
            'name': 'Updated Cottage',
            'max_guest': 6,
            'price_by_night': 120.75
        }
        updated_place = self.facade.update_place(place.id, updated_data)
        self.assertEqual(updated_place.name, 'Updated Cottage')
        self.assertEqual(updated_place.max_guest, 6)
        self.assertEqual(updated_place.price_by_night, 120.75)

    def test_update_place_invalid_data(self):
        place = self.facade.create_place(self.place_data)
        invalid_data = {'max_guest': -1}
        with self.assertRaises(ValueError):
            self.facade.update_place(place.id, invalid_data)

    def test_update_nonexistent_place(self):
        with self.assertRaises(ValueError):
            self.facade.update_place('nonexistent_id', {'name': 'New Name'})

    def test_get_all_places(self):
        self.facade.create_place(self.place_data)
        self.facade.create_place({**self.place_data, 'name': 'Another Place'})
        places = self.facade.get_all_places()
        self.assertEqual(len(places), 2)

    def test_get_places_by_city_existing(self):
        place1 = self.facade.create_place(self.place_data)
        place2 = self.facade.create_place({**self.place_data, 'city': 'Paris'})
        results = self.facade.get_places_by_city('Montreal')
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_get_places_by_city_nonexistent(self):
        results = self.facade.get_places_by_city('Nonexistent City')
        self.assertEqual(len(results), 0)

    def test_get_places_by_price_range(self):
        place1 = self.facade.create_place(self.place_data)
        place2 = self.facade.create_place({**self.place_data, 'price_by_night': 200})
        results = self.facade.get_places_by_price_range(90, 150)
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_get_places_by_capacity(self):
        place1 = self.facade.create_place(self.place_data)
        place2 = self.facade.create_place({**self.place_data, 'max_guest': 2})
        results = self.facade.get_places_by_capacity(4)
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_get_places_by_location(self):
        place1 = self.facade.create_place(self.place_data)
        place2 = self.facade.create_place({**self.place_data, 'latitude': 48.8566, 'longitude': 2.3522})  # Paris
        results = self.facade.get_places_by_location(45.5, -73.5, 10)  # 10 km radius
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_search_places(self):
        place1 = self.facade.create_place(self.place_data)
        place2 = self.facade.create_place({**self.place_data, 'name': 'Luxury Apartment', 'city': 'Paris'})
        results = self.facade.search_places('cozy')
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

if __name__ == '__main__':
    unittest.main()