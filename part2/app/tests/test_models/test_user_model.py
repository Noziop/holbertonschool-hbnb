import unittest
from models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('testuser', 'test@example.com', 'password123')

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_password_hashing(self):
        self.assertNotEqual(self.user.password_hash, 'password123')
        self.assertTrue(self.user.check_password('password123'))
        self.assertFalse(self.user.check_password('wrongpassword'))

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertIn('id', user_dict)
        self.assertIn('username', user_dict)
        self.assertIn('email', user_dict)
        self.assertNotIn('password_hash', user_dict)

if __name__ == '__main__':
    unittest.main()