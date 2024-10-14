import unittest
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from werkzeug.security import generate_password_hash, check_password_hash

class TestUser(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        User.repository = self.repository
        self.valid_params = {'username': 'patrickSebastion', 'email': 'blabla@blibli.bla', 'password': '&0(XGSr^0X'}
        self.user = User.create(**self.valid_params)

    def tearDown(self):
        User.repository = InMemoryRepository()

    def test_create(self):
        new_params = self.valid_params.copy()
        new_params['username'] = 'newuser'
        new_params['email'] = 'newuser@example.com'
        new_user = User.create(**new_params)
        self.assertIsInstance(new_user, User)
        self.assertIn(new_user.id, self.repository._storage)

    def test_create_with_existing_username(self):
        with self.assertRaises(ValueError):
            User.create(**self.valid_params)

    def test_create_with_existing_email(self):
        with self.assertRaises(ValueError):
            User.create(username='newuser', email=self.valid_params['email'], password='password123')

    def test_get_by_id(self):
        user = User.get_by_id(self.user.id)
        self.assertEqual(user.id, self.user.id)

        with self.assertRaises(ValueError):
            User.get_by_id('non_existent_id')

    def test_get_by_username(self):
        user = User.get_by_username(self.valid_params['username'])
        self.assertEqual(user.id, self.user.id)

        non_existent_user = User.get_by_username('non_existent_username')
        self.assertIsNone(non_existent_user)

    def test_get_by_email(self):
        user = User.get_by_email(self.valid_params['email'])
        self.assertEqual(user.id, self.user.id)

        non_existent_user = User.get_by_email('non_existent@email.com')
        self.assertIsNone(non_existent_user)

    def test_update(self):
        update_data = {'email': 'newemail@example.com', 'password': 'newpassword'}
        self.user.update(update_data)
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertTrue(self.user.check_password('newpassword'))

        with self.assertRaises(ValueError):
            self.user.update({'non_existent_attr': 'value'})

    def test_update_username(self):
        self.user.update({'username': 'newusername'})
        self.assertEqual(self.user.username, 'newusername')

        with self.assertRaises(ValueError):
            self.user.update({'username': 'a'})  # Too short

    def test_update_email(self):
        self.user.update({'email': 'newemail@example.com'})
        self.assertEqual(self.user.email, 'newemail@example.com')

        with self.assertRaises(ValueError):
            self.user.update({'email': 'invalid_email'})

    def test_delete(self):
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(ValueError):
            User.get_by_id(user_id)

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertIn('id', user_dict)
        self.assertIn('username', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)
        self.assertNotIn('password_hash', user_dict)

    def test_password_hashing(self):
        user = User.create(username='testuser', email='test@example.com', password='password123')
        self.assertNotEqual(user.password_hash, 'password123')
        self.assertTrue(user.check_password('password123'))

        user.update({'password': 'newpassword'})
        self.assertTrue(user.check_password('newpassword'))
        self.assertFalse(user.check_password('password123'))

    def test_validate_username(self):
        with self.assertRaises(ValueError):
            User.create(username='a', email='test@example.com', password='password')  # Too short
        with self.assertRaises(ValueError):
            User.create(username='a'*19, email='test@example.com', password='password')  # Too long
        with self.assertRaises(ValueError):
            User.create(username='invalid@username', email='test@example.com', password='password')  # Invalid characters

    def test_validate_email(self):
        with self.assertRaises(ValueError):
            User.create(username='validuser', email='invalidemail', password='password')
        with self.assertRaises(ValueError):
            User.create(username='validuser', email='invalid@email', password='password')

    def test_hash_password_exception(self):
        with self.assertRaises(ValueError):
            User.create(username='validuser', email='valid@email.com', password=None)

    def test_check_password_no_hash(self):
        user = User(username='testuser', email='test@example.com', password='password')
        user.password_hash = None
        with self.assertRaises(ValueError):
            user.check_password('password')

    def test_validate_username_type_error(self):
        with self.assertRaises(ValueError) as context:
            self.user._validate_username(123)
        self.assertEqual(str(context.exception), "Username must be a string")

    def test_validate_email_type_error(self):
        with self.assertRaises(ValueError) as context:
            self.user._validate_email(123)
        self.assertEqual(str(context.exception), "Email must be a string")

    def test_validate_email_invalid_domain(self):
        with self.assertRaises(ValueError) as context:
            self.user._validate_email("test@invalid")
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_validate_email_invalid_format(self):
        with self.assertRaises(ValueError) as context:
            self.user._validate_email("test@invalid.h")
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_init(self):
        user = User(username="testuser", email="test@example.com", password="password")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password"))

    def test_hash_password(self):
        hashed = self.user.hash_password("testpassword")
        self.assertNotEqual(hashed, "testpassword")
        self.assertTrue(check_password_hash(hashed, "testpassword"))

    def test_check_password(self):
        self.user.password_hash = generate_password_hash("testpassword")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_init_valid_data(self):
        user = User(username="testuser", email="test@example.com", password="password", first_name="Test", last_name="User", phone_number="+1234567890")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password"))
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "+1234567890")

    def test_init_invalid_username(self):
        with self.assertRaises(ValueError):
            User(username="a", email="test@example.com", password="password")

    def test_init_invalid_email(self):
        with self.assertRaises(ValueError):
            User(username="testuser", email="invalidemail", password="password")

    def test_init_invalid_phone_number(self):
        with self.assertRaises(ValueError):
            User(username="testuser", email="test@example.com", password="password", phone_number="invalidphone")

    def test_init_missing_username(self):
        with self.assertRaises(TypeError):
            User(email="test@example.com", password="password")

    def test_init_missing_email(self):
        with self.assertRaises(TypeError):
            User(username="testuser", password="password")

    def test_init_missing_password(self):
        with self.assertRaises(TypeError):
            User(username="testuser", email="test@example.com")

    def test_validate_phone_number(self):
        valid_phone_numbers = [
            "+1234567890",
            "1234567890",
            "+11234567890",
            "11234567890",
            "+33601020304"
        ]
        for phone_number in valid_phone_numbers:
            self.assertEqual(self.user._validate_phone_number(phone_number), phone_number)

        invalid_phone_numbers = [
            "12345",
            "abcdefghij",
            "+1234567890123456",  # Trop long
            "123456789",  # Trop court
            "+1234567a890"  # Contient une lettre
        ]
        for phone_number in invalid_phone_numbers:
            with self.assertRaises(ValueError):
                self.user._validate_phone_number(phone_number)


if __name__ == '__main__':
    unittest.main()