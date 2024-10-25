"""Test API Error Cases - Making our ghosts angry! 👻"""

import unittest
import json
import uuid
from app import create_app

class TestAPIErrors(unittest.TestCase):
    """Test all possible error cases in our API! 🧪"""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        # Préparer des données de test valides
        uuid_suffix = uuid.uuid4().hex[:6]
        self.valid_user = {
            'username': f'Ghost_{uuid_suffix}',
            'email': f'ghost_{uuid_suffix}@haunted.com',
            'password': 'GhostBoo123!',
            'first_name': 'Ghost',
            'last_name': 'Hunter'
        }

    def test_user_errors(self):
        """Test user endpoint errors 👻"""
        # Test création utilisateur avec données manquantes
        missing_data = {
            'email': 'ghost@test.com',
            'password': 'GhostBoo123!',
            'username': None,      # Ajout des champs manquants
            'first_name': None,
            'last_name': None
        }
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(missing_data)
        )
        self.assertEqual(response.status_code, 400)

        # Test email invalide
        invalid_email = self.valid_user.copy()
        invalid_email['email'] = 'not_an_email'
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(invalid_email)
        )
        self.assertEqual(response.status_code, 400)

        # Test username trop court
        short_username = self.valid_user.copy()
        short_username['username'] = 'short'
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(short_username)
        )
        self.assertEqual(response.status_code, 400)

        # Test mise à jour utilisateur inexistant
        response = self.client.put(
            '/api/v1/users/non-existent-id',
            headers=self.headers,
            data=json.dumps({'first_name': 'Updated'})
        )
        self.assertEqual(response.status_code, 400)

    def test_place_errors(self):
        """Test place endpoint errors 🏚️"""
        # Créer un utilisateur valide d'abord
        user_response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.valid_user)
        )
        user_id = user_response.json['id']

        # Test création place sans propriétaire
        invalid_place = {
            'name': 'Haunted Manor',
            'description': 'Spooky!',
            'price_by_night': 100
        }
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(invalid_place)
        )
        self.assertEqual(response.status_code, 400)

        # Test prix négatif
        negative_price = {
            'name': 'Haunted Manor',
            'description': 'Spooky!',
            'price_by_night': -100,
            'owner_id': user_id
        }
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(negative_price)
        )
        self.assertEqual(response.status_code, 400)

        # Test coordonnées invalides
        invalid_coords = {
            'name': 'Haunted Manor',
            'description': 'Spooky!',
            'price_by_night': 100,
            'owner_id': user_id,
            'latitude': 200,
            'longitude': -200
        }
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(invalid_coords)
        )
        self.assertEqual(response.status_code, 400)

    def test_amenity_errors(self):
        """Test amenity endpoint errors ✨"""
        # Test création sans nom
        invalid_amenity = {
            'description': 'No name here!'
        }
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.headers,
            data=json.dumps(invalid_amenity)
        )
        self.assertEqual(response.status_code, 400)

        # Test nom trop court
        short_name = {
            'name': 'a',
            'description': 'Too short!'
        }
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.headers,
            data=json.dumps(short_name)
        )
        self.assertEqual(response.status_code, 400)

        # Test mise à jour amenity inexistante
        response = self.client.put(
            '/api/v1/amenities/non-existent-id',
            headers=self.headers,
            data=json.dumps({'name': 'Updated'})
        )
        self.assertEqual(response.status_code, 400)

    def test_review_errors(self):
        """Test review endpoint errors 📝"""
        # Test création sans place_id et user_id
        invalid_review = {
            'text': 'Great place!',
            'rating': 5,
            'place_id': None,  # Ajout du place_id
            'user_id': None    # Ajout du user_id
        }

        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(invalid_review)
        )
        self.assertEqual(response.status_code, 400)

        # Test rating invalide
        invalid_rating = {
            'text': 'Great place!',
            'rating': 6,
            'place_id': 'some-id',
            'user_id': 'some-id'
        }
        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(invalid_rating)
        )
        self.assertEqual(response.status_code, 400)

        # Test suppression review inexistante
        response = self.client.delete('/api/v1/reviews/non-existent-id')
        self.assertEqual(response.status_code, 400)

        # Test création avec place inexistante
        invalid_review = {
            'text': 'Great place!',
            'rating': 5,
            'place_id': 'non-existent-id',
            'user_id': 'some-id'
        }
        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(invalid_review)
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()