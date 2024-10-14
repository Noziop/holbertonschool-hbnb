
import unittest
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class TestUser(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        User.repository = self.repository
        self.valid_params = {'username': 'patrickwilson', 'email': 'matthewvaughan@example.com', 'password': '&0(XGSr^0X'}
        self.user = User(**self.valid_params)

    def tearDown(self):
        User.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.user, attr))

    def test_methods(self):
        methods = ['check_password', 'create', 'delete', 'get_all', 'get_by_id', 'get_by_username', 'hash_password', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.user, method))

    def test_create(self):
        new_user = User.create(**self.valid_params)
        self.assertIsInstance(new_user, User)
        self.assertIn(new_user.id, self.repository._storage)

    def test_get_by_id(self):
        # Assurons-nous que l'utilisateur est bien ajouté au repository
        self.repository.add(self.user)
        user = User.get_by_id(self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.user, 'name') else None,
            'description': 'Updated Description' if hasattr(self.user, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.user.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.user, key), value)

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertIn('id', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            User(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.user.update({'invalid_param': 'invalid_value'})

    def test_password_hashing(self):
        user = User(**self.valid_params)
        self.assertNotEqual(user.password_hash, self.valid_params['password'])
        self.assertTrue(user.check_password(self.valid_params['password']))
        self.assertFalse(user.check_password('wrong_password'))

    def test_get_by_username(self):
        user = User.create(**self.valid_params)
        retrieved_user = User.get_by_username(self.valid_params['username'])
        self.assertEqual(user.id, retrieved_user.id)

    def test_get_all(self):
        user1 = User.create(**self.valid_params)
        user2 = User.create(username='user2', email='user2@example.com', password='password2')
        all_users = User.get_all()
        self.assertIn(user1, all_users)
        self.assertIn(user2, all_users)

    def test_delete(self):
        user = User.create(**self.valid_params)
        user_id = user.id
        user.delete()
        self.assertIsNone(User.get_by_id(user_id))

    def test_to_dict_no_password(self):
        user = User(**self.valid_params)
        user_dict = user.to_dict()
        self.assertNotIn('password', user_dict)
        self.assertNotIn('password_hash', user_dict)
        
    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
