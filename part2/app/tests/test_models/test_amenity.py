
import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.amenity = Amenity()  # Remove parameters for now

    def test_attributes(self):
        # Test that all attributes are present
        attrs = [('__class__', <class 'type'>), ('__dict__', mappingproxy({'__module__': 'app.models.amenity', '__init__': <function Amenity.__init__ at 0x7f79d2d08160>, 'to_dict': <function Amenity.to_dict at 0x7f79d2d083a0>, '__doc__': None})), ('__doc__', None), ('__module__', 'app.models.amenity'), ('__weakref__', <attribute '__weakref__' of 'BaseModel' objects>)]
        for attr in attrs:
            self.assertTrue(hasattr(self.amenity, attr[0]))

    def test_methods(self):
        # Test that all methods are present
        methods = []
        for method in methods:
            self.assertTrue(hasattr(self.amenity, method[0]))

    def test_to_dict(self):
        # Test the to_dict method
        model_dict = self.amenity.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

if __name__ == '__main__':
    unittest.main()
