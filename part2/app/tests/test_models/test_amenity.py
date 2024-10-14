
import unittest
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Amenity.repository = self.repository
        self.valid_params = {'name': 'blue join'}
        self.amenity = Amenity(**self.valid_params)
        self.repository.add(self.amenity)

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
        original_name = self.amenity.name
        new_name = 'Updated Name'
        original_updated_at = self.amenity.updated_at
        self.amenity.update({'name': new_name})
        self.assertEqual(self.amenity.name, new_name)
        self.assertNotEqual(self.amenity.name, original_name)
        self.assertNotEqual(self.amenity.updated_at, original_updated_at)

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

    def test_get_by_id_with_invalid_id(self):
        with self.assertRaises(ValueError):
            Amenity.get_by_id('invalid_id')

    def test_update_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.amenity.update('invalid_data')

    def test_name_validation(self):
        with self.assertRaises(ValueError):
            Amenity(name="")  # Nom vide
        with self.assertRaises(ValueError):
            Amenity(name="   ")  # Nom avec seulement des espaces
        with self.assertRaises(ValueError):
            Amenity(name="Invalid@Name")  # Nom avec caractères spéciaux non autorisés
        valid_name = "Pool-Area 123"
        amenity = Amenity(name=valid_name)
        self.assertEqual(amenity.name, valid_name)

    def test_get_all(self):
        amenity1 = Amenity.create(name="WiFi")
        amenity2 = Amenity.create(name="Parking")
        all_amenities = Amenity.get_all()
        self.assertIn(amenity1, all_amenities)
        self.assertIn(amenity2, all_amenities)

    def test_delete(self):
        amenity = Amenity.create(name="Gym")
        amenity_id = amenity.id
        amenity.delete()
        with self.assertRaises(ValueError):
            Amenity.get_by_id(amenity_id)

    def test_update_with_valid_params(self):
        amenity = Amenity(name="Pool")
        new_name = "Infinity Pool"
        amenity.update({'name': new_name})
        self.assertEqual(amenity.name, new_name)

    def test_to_dict_no_extra_attrs(self):
        amenity = Amenity(name="Sauna")
        amenity_dict = amenity.to_dict()
        expected_keys = {'id', 'name', 'created_at', 'updated_at'}
        self.assertEqual(set(amenity_dict.keys()), expected_keys)

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
