"""Test our user to_dict method 🧪"""

import unittest
import uuid
from app import create_app
from app.models.user import User

class TestUserToDict(unittest.TestCase):
    """Test the User to_dict transformation 📝"""

    def setUp(self):
        """Prepare our haunted laboratory! 🧪"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        
        # Créer un utilisateur de test
        uuid_suffix = uuid.uuid4().hex[:6]
        self.test_user = User(
            username=f'Ghost_{uuid_suffix}',
            email=f'ghost_{uuid_suffix}@haunted.com',
            password='GhostBoo123!',
            first_name='Ghost',
            last_name='Hunter'
        )

    def test_to_dict_excludes_password(self):
        """Test that to_dict excludes password fields 🔒"""
        # Convertir l'utilisateur en dictionnaire
        user_dict = self.test_user.to_dict()
        
        # Vérifier que les champs sensibles sont exclus
        self.assertNotIn('password', user_dict, 
                        "Password should not be in dictionary")
        self.assertNotIn('password_hash', user_dict, 
                        "Password hash should not be in dictionary")
        
        # Vérifier que les autres champs sont présents
        self.assertIn('username', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('first_name', user_dict)
        self.assertIn('last_name', user_dict)

if __name__ == '__main__':
    unittest.main()