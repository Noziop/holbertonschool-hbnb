
import unittest
from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Place.repository = self.repository
        self.valid_params = {'name': 'task', 'description': 'Issue work good body billion such. Popular opportunity evidence continue.\nItself leader do show important be write. Player billion ahead site decide require.\nDecision experience save organization next dinner while. Relationship force cultural management return. When small challenge wife.\nSister front a rest democratic serious college. Place reality own election move provide.\nExpert administration special prepare every song hear.', 'number_rooms': 8, 'number_bathrooms': 10, 'max_guest': 'laugh', 'price_by_night': 336.46, 'latitude': Decimal('59.4132055'), 'longitude': Decimal('-80.982168'), 'owner_id': 'a5aee83a-76b4-4350-a6db-42c6bdf2a8a2', 'city': 'our', 'country': 'benefit'}
        self.place = Place(**self.valid_params)

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

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
