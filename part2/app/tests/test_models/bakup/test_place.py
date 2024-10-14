
import unittest
from app.models.place import Place

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.place = Place(**{'name': 'test_name', 'description': 'test_description', 'number_rooms': 'test_number_rooms', 'number_bathrooms': 'test_number_bathrooms', 'max_guest': 'test_max_guest', 'price_by_night': 'test_price_by_night', 'latitude': 'test_latitude', 'longitude': 'test_longitude', 'city': 'test_city', 'country': 'test_country', 'owner_id': 'test_owner_id'})

    def test_attributes(self):
        attrs = []
        for attr in attrs:
            self.assertTrue(hasattr(self.place, attr))

    def test_methods(self):
        methods = ['add_amenity', 'add_review', 'save', 'set_owner', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.place, method))

    def test_to_dict(self):
        model_dict = self.place.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

if __name__ == '__main__':
    unittest.main()
