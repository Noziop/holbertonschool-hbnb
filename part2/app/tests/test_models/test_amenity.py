
import unittest
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Amenity.repository = self.repository
        self.valid_params = {'name': 'road player'}
        self.amenity = Amenity(**self.valid_params)

    def tearDown(self):
        Amenity.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.amenity, attr))

    def test_methods(self):
        methods = ['_validate_name', 'create', 'delete', 'get_all', 'get_by_id', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.amenity, method))

    def test_create(self):
        new_amenity = Amenity.create(**self.valid_params)
        self.assertIsInstance(new_amenity, Amenity)
        self.assertIn(new_amenity.id, self.repository._storage)

    def test_get_by_id(self):
        amenity = Amenity.get_by_id(self.amenity.id)
        self.assertEqual(amenity.id, self.amenity.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.amenity, 'name') else None,
            'description': 'Updated Description' if hasattr(self.amenity, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.amenity.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.amenity, key), value)

    def test_to_dict(self):
        amenity_dict = self.amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertIn('id', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            Amenity(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.amenity.update({'invalid_param': 'invalid_value'})

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
