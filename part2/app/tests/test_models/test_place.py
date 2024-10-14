
import unittest
from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from decimal import Decimal

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Place.repository = self.repository
        self.valid_params = {'name': 'lay', 'description': 'Mrs nice example without common product. Career final possible under. Television leave let detail same.\nCareer much fly present. Color fly us executive country turn.\nFight during exist effort into stage care right.\nMajor cup once. Nor study strong million citizen. Improve painting which bank.\nGrow property phone. Couple actually cold office kind choose including. Such light public beyond feel control step.\nPretty stop prove rather. Take draw all article meet yet. Magazine simply bed eight.', 'number_rooms': 3, 'number_bathrooms': 8, 'max_guest': 5, 'price_by_night': 25.31, 'latitude': Decimal('-58.8818915'), 'longitude': Decimal('-93.856037'), 'owner_id': '68f18302-34ef-4189-9259-d9e1a669c73e', 'city': 'economy', 'country': 'worker'}
        self.place = Place(**self.valid_params)
        self.repository.add(self.place)

    def tearDown(self):
        Place.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.place, attr))

    def test_methods(self):
        methods = ['_validate_latitude', '_validate_longitude', '_validate_positive_float', '_validate_positive_integer', 'add_amenity_id', 'add_review_id', 'create', 'delete', 'get_all', 'get_by_id', 'remove_amenity_id', 'remove_review_id', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.place, method))

    def test_create(self):
        new_place = Place.create(**self.valid_params)
        self.assertIsInstance(new_place, Place)
        self.assertIn(new_place.id, self.repository._storage)

    def test_get_by_id(self):
        place = Place.get_by_id(self.place.id)
        self.assertEqual(place.id, self.place.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.place, 'name') else None,
            'description': 'Updated Description' if hasattr(self.place, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.place.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.place, key), value)

    def test_update_name_n_maxguest(self):
        update_data = {
            'name': 'Updated Name',
            'max_guest': 10
        }
        self.place.update(update_data)
        self.assertEqual(self.place.name, 'Updated Name')
        self.assertEqual(self.place.max_guest, 10)

    def test_to_dict(self):
        place_dict = self.place.to_dict()
        self.assertIsInstance(place_dict, dict)
        self.assertIn('id', place_dict)
        self.assertIn('created_at', place_dict)
        self.assertIn('updated_at', place_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            Place(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.place.update({'invalid_param': 'invalid_value'})
        with self.assertRaises(ValueError):
            self.place.update({'max_guest': -1})
        with self.assertRaises(ValueError):
            self.place.update({'latitude': 100})

    def test_invalid_max_guest(self):
        with self.assertRaises(ValueError):
            Place(**{**self.valid_params, 'max_guest': 'invalid'})

    def test_invalid_price_by_night(self):
        with self.assertRaises(ValueError):
            Place(**{**self.valid_params, 'price_by_night': -10})

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Place(**{**self.valid_params, 'latitude': 100})

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Place(**{**self.valid_params, 'longitude': 200})

    def test_add_remove_amenity(self):
        amenity_id = "test_amenity_id"
        self.place.add_amenity_id(amenity_id)
        self.assertIn(amenity_id, self.place.amenity_ids)
        self.place.remove_amenity_id(amenity_id)
        self.assertNotIn(amenity_id, self.place.amenity_ids)

    def test_add_remove_review(self):
        review_id = "test_review_id"
        self.place.add_review_id(review_id)
        self.assertIn(review_id, self.place.review_ids)
        self.place.remove_review_id(review_id)
        self.assertNotIn(review_id, self.place.review_ids)

    def test_delete(self):
        place = Place.create(**self.valid_params)
        place_id = place.id
        place.delete()
        with self.assertRaises(ValueError):
            place.get_by_id(place_id)

    def test_get_all(self):
        place1 = Place.create(**self.valid_params)
        place2 = Place.create(**self.valid_params)
        all_places = Place.get_all()
        self.assertIn(place1, all_places)
        self.assertIn(place2, all_places)

    def test_get_by_id_with_invalid_id(self):
        with self.assertRaises(ValueError):
            Place.get_by_id('invalid_id')
    
    def test_update_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.place.update('invalid_data')

    def test_update_additional_attributes(self):
        update_data = {
            'number_rooms': 5,
            'number_bathrooms': 3,
            'price_by_night': 100.50,
            'longitude': 45.5,
            'latitude': 30.2
        }
        self.place.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.place, key), value)

    def test_update_with_non_dict(self):
        with self.assertRaises(ValueError):
            self.place.update("Not a dictionary")

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
