import unittest
from app.services.facade import HBnBFacade
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class TestUserFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def tearDown(self):
        User.repository = InMemoryRepository()

    def test_create_user(self):
        user = self.facade.create_user(self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_get_user(self):
        created_user = self.facade.create_user(self.user_data)
        retrieved_user = self.facade.get_user(created_user.id)
        self.assertEqual(created_user.id, retrieved_user.id)
        self.assertEqual(retrieved_user.username, 'testuser')

    def test_get_user_by_username(self):
        self.facade.create_user(self.user_data)
        user = self.facade.get_user_by_username('testuser')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')

    def test_get_user_by_email(self):
        self.facade.create_user(self.user_data)
        user = self.facade.get_user_by_email('test@example.com')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@example.com')

    def test_update_user(self):
        user = self.facade.create_user(self.user_data)
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        updated_user = self.facade.update_user(user.id, updated_data)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_get_all_users(self):
        self.facade.create_user(self.user_data)
        self.facade.create_user({**self.user_data, 'username': 'testuser2', 'email': 'test2@example.com'})
        users = self.facade.get_all_users()
        self.assertEqual(len(users), 2)

    def test_check_user_password(self):
        user = self.facade.create_user(self.user_data)
        self.assertTrue(self.facade.check_user_password(user.id, 'password123'))
        self.assertFalse(self.facade.check_user_password(user.id, 'wrongpassword'))

    def test_create_user_with_existing_username(self):
        self.facade.create_user(self.user_data)
        with self.assertRaises(ValueError):
            self.facade.create_user(self.user_data)

    def test_create_user_with_existing_email(self):
        self.facade.create_user(self.user_data)
        with self.assertRaises(ValueError):
            self.facade.create_user({**self.user_data, 'username': 'newuser'})

    def test_get_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.facade.get_user('nonexistent_id')

    def test_update_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.facade.update_user('nonexistent_id', {'first_name': 'Updated'})

if __name__ == '__main__':
    unittest.main()