
import unittest
from app.models.basemodel import BaseModel

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.basemodel = BaseModel()

    def test_attributes(self):
        attrs = []
        for attr in attrs:
            self.assertTrue(hasattr(self.basemodel, attr))

    def test_methods(self):
        methods = ['save', 'to_dict']
        for method in methods:
            self.assertTrue(hasattr(self.basemodel, method))

    def test_to_dict(self):
        model_dict = self.basemodel.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

if __name__ == '__main__':
    unittest.main()
