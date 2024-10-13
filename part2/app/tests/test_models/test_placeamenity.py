
import unittest
from app.models.placeamenity import PlaceAmenity
from app.persistence.repository import InMemoryRepository

class TestPlaceAmenity(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        PlaceAmenity.repository = self.repository
        self.valid_params = {'place_id': '3b746ac5-f8f9-4e8f-a2f4-ef46c15ba5b0', 'amenity_id': '95a7f825-7b2e-42e0-bfc3-78510288fce2'}
        self.placeamenity = PlaceAmenity(**self.valid_params)

    def tearDown(self):
        PlaceAmenity.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.placeamenity, attr))

    def test_methods(self):
        methods = ['_validate_id', 'create', 'delete', 'get_all', 'get_by_amenity', 'get_by_id', 'get_by_place', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.placeamenity, method))

    def test_create(self):
        new_placeamenity = PlaceAmenity.create(**self.valid_params)
        self.assertIsInstance(new_placeamenity, PlaceAmenity)
        self.assertIn(new_placeamenity.id, self.repository._storage)

    def test_get_by_id(self):
        placeamenity = PlaceAmenity.get_by_id(self.placeamenity.id)
        self.assertEqual(placeamenity.id, self.placeamenity.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.placeamenity, 'name') else None,
            'description': 'Updated Description' if hasattr(self.placeamenity, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.placeamenity.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.placeamenity, key), value)

    def test_to_dict(self):
        placeamenity_dict = self.placeamenity.to_dict()
        self.assertIsInstance(placeamenity_dict, dict)
        self.assertIn('id', placeamenity_dict)
        self.assertIn('created_at', placeamenity_dict)
        self.assertIn('updated_at', placeamenity_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            PlaceAmenity(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.placeamenity.update({'invalid_param': 'invalid_value'})

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
