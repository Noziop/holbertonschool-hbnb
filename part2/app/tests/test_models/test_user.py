"""Test module for User class. Bring the sass! 💅"""
import unittest
from app.models.user import User


class TestUser(unittest.TestCase):
    """Test cases for User class. Let's spill the tea! ☕"""

    def setUp(self):
        """Set up test cases. Preparing the runway! 🎭"""
        self.test_data = {
            'username': 'FabulousUser',
            'email': 'fabulous@test.com',
            'password': 'Password123!',
            'first_name': 'Fabulous',
            'last_name': 'Queen',
            'phone_number': '+1234567890'
        }
        self.user = User.create(**self.test_data)

    def test_initialization(self):
        """Test User initialization. Birth of a queen! 👑"""
        self.assertEqual(self.user.username, 'FabulousUser')
        self.assertEqual(self.user.email, 'fabulous@test.com')
        self.assertTrue(self.user.check_password('Password123!'))
        
        # Test validation errors with attitude
        with self.assertRaises(ValueError):
            User.create(username='tiny', **{
                k:v for k,v in self.test_data.items() if k != 'username'
            })
        with self.assertRaises(ValueError):
            User.create(password='weak', **{
                k:v for k,v in self.test_data.items() if k != 'password'
            })

    def test_password_validation(self):
        """Test password validation. No basic passwords allowed! 💪"""
        weak_passwords = [
            'short',  # Too short, like my patience
            'nouppercase123!',  # Missing uppercase, like my standards
            'NOLOWERCASE123!',  # Missing lowercase, how crude
            'NoSpecialChar123',  # Missing special char, boring!
            'NoNumber!!!'  # Missing number, really queen?
        ]
        
        for password in weak_passwords:
            with self.assertRaises(ValueError):
                User.create(**{**self.test_data, 'password': password})

    def test_unique_constraints(self):
        """Test uniqueness. No copycats allowed! 🐱"""
        # Try to create user with same username
        with self.assertRaises(ValueError):
            User.create(**self.test_data)
        
        # Try with same email
        modified_data = dict(self.test_data)
        modified_data['username'] = 'AnotherFabUser'
        with self.assertRaises(ValueError):
            User.create(**modified_data)

    def test_update(self):
        """Test update functionality. Glow up time! ✨"""
        update_data = {
            'username': 'EvenMoreFabulous',
            'email': 'more.fabulous@test.com',
            'password': 'NewPassword123!'
        }
        
        updated_user = self.user.update(update_data)
        self.assertEqual(updated_user.username, 'EvenMoreFabulous')
        self.assertEqual(updated_user.email, 'more.fabulous@test.com')
        self.assertTrue(updated_user.check_password('NewPassword123!'))

    def test_search(self):
        """Test search functionality. Find that queen! 👸"""
        # Create some more users for testing
        User.create(**{
            **self.test_data,
            'username': 'AnotherQueen',
            'email': 'another@test.com'
        })
        
        results = User.search(first_name='Fabulous')
        self.assertEqual(len(results), 2)

    def test_phone_validation(self):
        """Test phone validation. No fake numbers, honey! 📱"""
        invalid_phones = [
            'not-a-number',  # Obviously, duh!
            '123',  # Too short, like my patience
            '123456789012345',  # Too long, like my ex's stories
            '+abc1234567890'  # Letters in phone? Who raised you?
        ]
        
        for phone in invalid_phones:
            with self.assertRaises(ValueError):
                User.create(**{**self.test_data, 'phone_number': phone})

    def test_name_validation(self):
        """Test name validation. Keep it classy! 💅"""
        invalid_names = [
            '1',  # Too short
            'a' * 51,  # Too long, like this week
            'Name123',  # Numbers? In MY name?
            'Name@Special'  # Special chars are for passwords only!
        ]
        
        for name in invalid_names:
            with self.assertRaises(ValueError):
                User.create(**{
                    **self.test_data,
                    'first_name': name
                })

    def test_edge_cases(self):
        """Test edge cases. Pushing boundaries like a true queen! 👑"""
        # Test empty strings
        with self.assertRaises(ValueError):
            User.create(**{**self.test_data, 'username': ''})
        
        # Test None values
        with self.assertRaises(ValueError):
            User.create(**{**self.test_data, 'email': None})
        
        # Test spaces only
        with self.assertRaises(ValueError):
            User.create(**{**self.test_data, 'first_name': '   '})

    def test_password_hash_errors(self):
        """Test password hashing. Keeping secrets since forever! 🔐"""
        # Test check_password avec un hash manquant
        user = User(**self.test_data)
        user.password_hash = None
        with self.assertRaises(ValueError):
            user.check_password('any_password')
        
        # Test avec un mot de passe invalide
        with self.assertRaises(ValueError):
            self.user._validate_password('')  # Password vide
        with self.assertRaises(ValueError):
            self.user._validate_password('weak')  # Password trop faible

    def test_to_dict(self):
        """Test serialization. Expose everything... except the secrets! 🤫"""
        user_dict = self.user.to_dict()
        
        # Check all the tea is there
        self.assertIn('username', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('first_name', user_dict)
        
        # But not the password hash, we're not that messy! 💅
        self.assertNotIn('password_hash', user_dict)

    def tearDown(self):
        """Clean up after tests. Leave no traces, like a true queen! 👑"""
        User.repository._storage.clear()

    def test_username_validation_extra_sass(self):
        """Test username validation with EXTRA sass! 💅"""
        invalid_usernames = [
            123,  # Not a string, honey!
            'smol',  # Too short (like my temper)
            'waaaaaaaaytooooooolong',  # Too long (like my ex's stories)
            'User@Name#Special'  # Special chars? In MY username?
        ]
        
        for username in invalid_usernames:
            with self.assertRaises(ValueError):
                User.create(**{**self.test_data, 'username': username})

    def test_name_validation_full_fantasy(self):
        """Test name validation with full fantasy! 🌈"""
        invalid_cases = [
            (123, "numeric fantasy"),  # Numbers aren't names, sweetie
            ('x', "too short"),  # Like my coffee breaks
            ('a' * 51, "too long"),  # Like my shopping receipts
            ('Name123!@#', "special chars")  # Save the drama for your password
        ]
        
        for name, case in invalid_cases:
            with self.assertRaises(ValueError):
                User.create(**{**self.test_data, 'first_name': name})

    def test_search_empty_criteria(self):
        """Test search with no criteria, show me EVERYBODY! 👀"""
        result = User.search()  # Get all users, spill ALL the tea!
        self.assertIsInstance(result, list)
        self.assertIn(self.user, result)

    def test_update_invalid_attributes(self):
        """Test update with invalid attributes. Nice try, honey! 🙄"""
        invalid_updates = {
            'not_an_attribute': 'value',  # Who do you think you are?
            'fake_field': 123  # Not in MY database!
        }
        
        for key, value in invalid_updates.items():
            with self.assertRaises(ValueError):
                self.user.update({key: value})

    def test_update_duplicate_credentials(self):
        """Test update with taken credentials. No copycats allowed! 🐱"""
        # Create another user
        other_user = User.create(
            username='OtherQueen',
            email='other@test.com',
            password='Password123!',
            first_name='Other',
            last_name='Queen'
        )
        
        # Try to update to existing username
        with self.assertRaises(ValueError):
            self.user.update({'username': 'OtherQueen'})
        
        # Try to update to existing email
        with self.assertRaises(ValueError):
            self.user.update({'email': 'other@test.com'})


if __name__ == '__main__':
    unittest.main()