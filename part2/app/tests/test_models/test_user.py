import unittest
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from werkzeug.security import generate_password_hash, check_password_hash

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        self.valid_user_data = {
            'username': 'validuser',
            'email': 'validuser@example.com',
            'password': 'ValidPass123!',
            'first_name': 'Valid',
            'last_name': 'User',
            'phone_number': '+12345678901'
        }

    def test_user_creation_with_valid_data(self):
        user = User(**self.valid_user_data)
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(user.email, self.valid_user_data['email'])
        self.assertTrue(check_password_hash(user.password_hash, self.valid_user_data['password']))
        self.assertEqual(user.first_name, self.valid_user_data['first_name'])
        self.assertEqual(user.last_name, self.valid_user_data['last_name'])
        self.assertEqual(user.phone_number, self.valid_user_data['phone_number'])

    def test_user_creation_with_missing_data(self):
        invalid_user_data = self.valid_user_data.copy()
        invalid_user_data.pop('username')
        with self.assertRaises(ValueError):
            User(**invalid_user_data)

    def test_username_validation(self):
        with self.assertRaises(ValueError):
            User._validate_username('short')
        with self.assertRaises(ValueError):
            User._validate_username('thisusernameiswaytoolong')
        with self.assertRaises(ValueError):
            User._validate_username('invalid username!')

    def test_password_validation(self):
        with self.assertRaises(ValueError):
            User._validate_password('short')
        with self.assertRaises(ValueError):
            User._validate_password('NoNumber!')
        with self.assertRaises(ValueError):
            User._validate_password('nonumber123!')
        with self.assertRaises(ValueError):
            User._validate_password('NOLOWERCASE123!')
        with self.assertRaises(ValueError):
            User._validate_password('nouppercase123!')
        with self.assertRaises(ValueError):
            User._validate_password('NoSpecialChar123')

    def test_email_validation(self):
        with self.assertRaises(ValueError):
            User._validate_email('invalidemail.com')
        with self.assertRaises(ValueError):
            User._validate_email('invalid@com')
        with self.assertRaises(ValueError):
            User._validate_email('invalid@.com')

    def test_name_validation(self):
        with self.assertRaises(ValueError):
            User._validate_name('A', 'First name')
        with self.assertRaises(ValueError):
            User._validate_name('ThisNameIsWayTooLongToBeValidBecauseItExceedsFiftyCharacters', 'First name')
        with self.assertRaises(ValueError):
            User._validate_name('Invalid123', 'First name')

    def test_phone_number_validation(self):
        with self.assertRaises(ValueError):
            User._validate_phone_number('12345')
        with self.assertRaises(ValueError):
            User._validate_phone_number('invalidphone')

    def test_hash_password(self):
        user = User(**self.valid_user_data)
        self.assertTrue(check_password_hash(user.password_hash, self.valid_user_data['password']))

    def test_check_password(self):
        user = User(**self.valid_user_data)
        self.assertTrue(user.check_password(self.valid_user_data['password']))
        self.assertFalse(user.check_password('WrongPassword123!'))

    def test_create_user(self):
        user = User.create(**self.valid_user_data)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.valid_user_data['username'])

    def test_create_user_with_existing_username(self):
        User.create(**self.valid_user_data)
        with self.assertRaises(ValueError):
            User.create(**self.valid_user_data)

    def test_create_user_with_existing_email(self):
        User.create(**self.valid_user_data)
        new_user_data = self.valid_user_data.copy()
        new_user_data['username'] = 'newusername'
        with self.assertRaises(ValueError):
            User.create(**new_user_data)

    def test_update_user(self):
        user = User.create(**self.valid_user_data)
        update_data = {'username': 'newusername', 'email': 'newemail@example.com'}
        user.update(update_data)
        self.assertEqual(user.username, 'newusername')
        self.assertEqual(user.email, 'newemail@example.com')

    def test_update_user_with_existing_username(self):
        User.create(**self.valid_user_data)
        user = User.create(username='newuser', email='newuser@example.com', password='NewPass123!', first_name='New', last_name='User')
        with self.assertRaises(ValueError):
            user.update({'username': 'validuser'})

    def test_update_user_with_existing_email(self):
        User.create(**self.valid_user_data)
        user = User.create(username='newuser', email='newuser@example.com', password='NewPass123!', first_name='New', last_name='User')
        with self.assertRaises(ValueError):
            user.update({'email': 'validuser@example.com'})

    def test_to_dict(self):
        user = User.create(**self.valid_user_data)
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], self.valid_user_data['username'])
        self.assertEqual(user_dict['email'], self.valid_user_data['email'])
        self.assertEqual(user_dict['first_name'], self.valid_user_data['first_name'])
        self.assertEqual(user_dict['last_name'], self.valid_user_data['last_name'])
        self.assertEqual(user_dict['phone_number'], self.valid_user_data['phone_number'])
        self.assertNotIn('password_hash', user_dict)

if __name__ == '__main__':
    unittest.main()