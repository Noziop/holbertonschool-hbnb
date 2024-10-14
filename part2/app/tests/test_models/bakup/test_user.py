
import unittest
from app.models.user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(**{'username': 'test_username', 'email': 'test_email', 'password': 'test_password'})

    def test_attributes(self):
        attrs = []
        for attr in attrs:
            self.assertTrue(hasattr(self.user, attr))

    def test_methods(self):
        methods = ['check_password', 'hash_password', 'save', 'to_dict']
        for method in methods:
            self.assertTrue(hasattr(self.user, method))

    def test_to_dict(self):
        model_dict = self.user.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

if __name__ == '__main__':
    unittest.main()
