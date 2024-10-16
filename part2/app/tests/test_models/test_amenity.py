import unittest
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Amenity.repository = self.repository
        self.valid_params = {
            'name': 'Wi-Fi'
        }
        self.amenity = Amenity.create(**self.valid_params)

    def tearDown(self):
        Amenity.repository = InMemoryRepository()

    def test_create(self):
        new_amenity = Amenity.create(**self.valid_params)
        self.assertIsInstance(new_amenity, Amenity)
        self.assertIn(new_amenity.id, self.repository._storage)

    def test_create_with_invalid_params(self):
        invalid_params = {'name': ''}
        with self.assertRaises(ValueError):
            Amenity.create(**invalid_params)

    def test_get_by_id(self):
        amenity = Amenity.get_by_id(self.amenity.id)
        self.assertEqual(amenity.id, self.amenity.id)

    def test_get_by_id_nonexistent(self):
        with self.assertRaises(ValueError):
            Amenity.get_by_id('nonexistent_id')

    def test_get_all(self):
        amenities = Amenity.get_all()
        self.assertIn(self.amenity, amenities)

    def test_update(self):
        update_data = {'name': 'Updated Wi-Fi'}
        self.amenity.update(update_data)
        self.assertEqual(self.amenity.name, 'Updated Wi-Fi')

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.amenity.update({'invalid_param': 'invalid_value'})
        with self.assertRaises(ValueError):
            self.amenity.update({'name': ''})

    def test_to_dict(self):
        amenity_dict = self.amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertIn('id', amenity_dict)
        self.assertIn('name', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)

    def test_get_by_name(self):
        amenity1 = Amenity.create(name='Pool')
        amenity2 = Amenity.create(name='Gym')
        
        results = Amenity.get_by_name('Pool')
        self.assertIn(amenity1, results)
        self.assertNotIn(amenity2, results)

    def test_search(self):
        amenity1 = Amenity.create(name='Swimming Pool')
        amenity2 = Amenity.create(name='Fitness Center')
        
        results = Amenity.search('pool')
        self.assertIn(amenity1, results)
        self.assertNotIn(amenity2, results)

    def test_validate_name(self):
        with self.assertRaises(ValueError):
            Amenity._validate_name('')
        with self.assertRaises(ValueError):
            Amenity._validate_name('Invalid@Name')
        
        valid_name = Amenity._validate_name('Valid Name-123')
        self.assertEqual(valid_name, 'Valid Name-123')

if __name__ == '__main__':
    unittest.main()