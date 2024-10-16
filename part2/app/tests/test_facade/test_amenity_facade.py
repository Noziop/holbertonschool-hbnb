import unittest
from app.services.facade import HBnBFacade
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestAmenityFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()
        self.amenity_data = {
            'name': 'Wi-Fi'
        }

    def tearDown(self):
        Amenity.repository = InMemoryRepository()

    def test_create_amenity_valid(self):
        amenity = self.facade.create_amenity(self.amenity_data)
        self.assertIsInstance(amenity, Amenity)
        self.assertEqual(amenity.name, 'Wi-Fi')

    def test_create_amenity_invalid_name(self):
        invalid_data = {'name': ''}
        with self.assertRaises(ValueError):
            self.facade.create_amenity(invalid_data)

    def test_get_amenity_existing(self):
        created_amenity = self.facade.create_amenity(self.amenity_data)
        retrieved_amenity = self.facade.get_amenity(created_amenity.id)
        self.assertEqual(created_amenity.id, retrieved_amenity.id)

    def test_get_amenity_nonexistent(self):
        with self.assertRaises(ValueError):
            self.facade.get_amenity('nonexistent_id')

    def test_update_amenity_valid(self):
        amenity = self.facade.create_amenity(self.amenity_data)
        updated_data = {'name': 'High-Speed Wi-Fi'}
        updated_amenity = self.facade.update_amenity(amenity.id, updated_data)
        self.assertEqual(updated_amenity.name, 'High-Speed Wi-Fi')

    def test_update_amenity_invalid_name(self):
        amenity = self.facade.create_amenity(self.amenity_data)
        invalid_data = {'name': ''}
        with self.assertRaises(ValueError):
            self.facade.update_amenity(amenity.id, invalid_data)

    def test_update_nonexistent_amenity(self):
        with self.assertRaises(ValueError):
            self.facade.update_amenity('nonexistent_id', {'name': 'New Name'})

    def test_get_all_amenities(self):
        self.facade.create_amenity(self.amenity_data)
        self.facade.create_amenity({'name': 'Pool'})
        amenities = self.facade.get_all_amenities()
        self.assertEqual(len(amenities), 2)

    def test_get_amenities_by_name(self):
        self.facade.create_amenity(self.amenity_data)
        self.facade.create_amenity({'name': 'Pool'})
        results = self.facade.get_amenities_by_name('Wi-Fi')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Wi-Fi')

    def test_search_amenities(self):
        self.facade.create_amenity(self.amenity_data)
        self.facade.create_amenity({'name': 'Swimming Pool'})
        results = self.facade.search_amenities('pool')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Swimming Pool')

    def test_get_places_with_amenity(self):
        amenity = self.facade.create_amenity(self.amenity_data)
        
        place_data = {
            "name": "Test Place",
            "description": "Test Description",
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "price_by_night": 100,
            "latitude": 45.5,
            "longitude": -73.5,
            "owner_id": "test_owner"
        }
        place = self.facade.create_place(place_data)
        
        self.facade.add_amenity_to_place(place.id, amenity.id)

        places = self.facade.get_places_with_amenity(amenity.id)
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0].id, place.id)

if __name__ == '__main__':
    unittest.main()