
import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.amenity = Amenity(**{'name': 'test_name'})

    def test_attributes(self):
        attrs = []
        for attr in attrs:
            self.assertTrue(hasattr(self.amenity, attr))

    def test_methods(self):
        methods = ['save', 'to_dict']
        for method in methods:
            self.assertTrue(hasattr(self.amenity, method))

    def test_to_dict(self):
        model_dict = self.amenity.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

if __name__ == '__main__':
    unittest.main()
