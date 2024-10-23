"""Test module for User class. Spooky testing time! 👻"""
import unittest
import uuid
from app.models.user import User


class TestUser(unittest.TestCase):
    """Test cases for User class. Let's summon some test spirits! 🧙‍♀️"""

    def setUp(self):
        """Prepare our haunted test environment! 🏚️"""
        self.unique_id = str(uuid.uuid4())[:6]
        
        # Our test data - like ingredients for a spell! 🔮
        self.test_data = {
            'username': f'Ghost_{self.unique_id}',
            'email': f'ghost_{self.unique_id}@haunted.com',
            'password': 'Haunted123!',
            'first_name': 'Spooky',
            'last_name': 'Spirit',
            'phone_number': '+1234567890'
        }
        
        # Create our test user - summon the spirit! 👻
        self.user = User.create(**self.test_data)

    def test_initialization(self):
        """Test User initialization. Birth of a spirit! 👻"""
        self.assertEqual(self.user.username, f'Ghost_{self.unique_id}')
        self.assertEqual(self.user.email, f'ghost_{self.unique_id}@haunted.com')
        self.assertTrue(self.user.check_password('Haunted123!'))
        
        # Test validation errors - when the spirits reject you! 👻
        with self.assertRaises(ValueError):
            User.create(**{
                **self.test_data,
                'username': 'tiny'  # Too short to haunt!
            })

    def test_password_validation(self):
        """Test password validation. Supernatural security check! 🔐"""
        weak_passwords = [
            'short',  # Too short for the afterlife
            'nouppercase123!',  # Ghosts demand CAPS!
            'NOLOWERCASE123!',  # Even spirits need lowercase
            'NoSpecialChar123',  # Where's the supernatural symbols?
            'NoNumber!!!'  # Numbers are sacred!
        ]
        
        for password in weak_passwords:
            with self.assertRaises(ValueError):
                User.create(**{**self.test_data, 'password': password})

    def test_unique_constraints(self):
        """Test uniqueness. Each spirit must be unique! 👻"""
        # Try to create a doppelganger
        with self.assertRaises(ValueError):
            User.create(**self.test_data)
        
        # Try with same email but different username
        new_unique_id = str(uuid.uuid4())[:6]
        with self.assertRaises(ValueError):
            User.create(**{
                **self.test_data,
                'username': f'Phantom_{new_unique_id}'
            })

    def test_update(self):
        """Test update functionality. Spirit makeover time! ✨"""
        new_unique_id = str(uuid.uuid4())[:6]
        update_data = {
            'username': f'Updated_{new_unique_id}',
            'email': f'updated_{new_unique_id}@haunted.com',
            'password': 'UpdatedHaunted123!'
        }
        
        updated_user = self.user.update(update_data)
        self.assertEqual(updated_user.username, f'Updated_{new_unique_id}')
        self.assertEqual(updated_user.email, f'updated_{new_unique_id}@haunted.com')
        self.assertTrue(updated_user.check_password('UpdatedHaunted123!'))

    def test_search(self):
        """Test search functionality. Ghost hunting time! 👻"""
        # Create another spirit for testing
        another_unique_id = str(uuid.uuid4())[:6]
        User.create(**{
            **self.test_data,
            'username': f'Spirit_{another_unique_id}',
            'email': f'spirit_{another_unique_id}@haunted.com'
        })
        
        # Search by first_name
        results = User.search(first_name='Spooky')
        self.assertGreaterEqual(len(results), 1)

    def test_to_dict(self):
        """Test serialization. Materializing spirit data! 📜"""
        user_dict = self.user.to_dict()
        
        # Check all required attributes are present
        required_fields = ['username', 'email', 'first_name', 'last_name']
        for field in required_fields:
            self.assertIn(field, user_dict)
        
        # Password hash should remain in the spirit realm
        self.assertNotIn('password_hash', user_dict)

    def tearDown(self):
        """Clean up our haunted test environment! 🧹"""
        User.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()