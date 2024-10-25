"""API Test Suite - Let's make sure our haunted API works perfectly! 👻"""

import unittest
import json, uuid
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestAPI(unittest.TestCase):
    """Test our spooky API endpoints! 🧪"""

    def setUp(self):
        """Prepare our haunted laboratory! 🧪"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        # UUID de 6 caractères pour respecter la limite de 12 caractères
        uuid_suffix = uuid.uuid4().hex[:6]
        
        # Test user avec un mot de passe qui respecte les critères :
        # - 8 caractères minimum
        # - 1 majuscule
        # - 1 chiffre
        # - 1 caractère spécial
        self.test_user = {
            'username': f'Ghost_{uuid_suffix}',  # Entre 6 et 12 caractères
            'email': f'ghost_{uuid_suffix}@haunted.com',
            'password': 'GhostBoo123!',  # Respecte tous les critères
            'first_name': 'Ghost',
            'last_name': 'Hunter'
        }

        # Test invalid user pour le test d'erreur
        self.invalid_user = {
            'username': f'Ghost_{uuid_suffix}',
            'email': f'ghost_{uuid_suffix}@haunted.com',
            'password': 'weak',  # Ne respecte pas les critères
            'first_name': 'Ghost',
            'last_name': 'Hunter'
        }

        self.test_place = {
            'name': 'Haunted Manor',
            'description': 'A very spooky place!',
            'number_rooms': 5,
            'number_bathrooms': 3,
            'max_guest': 10,
            'price_by_night': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'city': 'Ghost Town',
            'state': 'Haunted State',
            'address': '666 Spooky Lane'
        }

        self.test_amenity = {
            'name': 'Ghost Detector',
            'description': 'Detects supernatural activity'
        }

        self.test_review = {
            'text': 'Super spooky, loved it!',
            'rating': 5
        }

    def test_user_endpoints(self):
        """Test our user management endpoints 👤"""
        # Test CREATE user
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.test_user)
        )
        self.assertEqual(response.status_code, 201)
        user_id = response.json['id']

        # Vérifie que l'utilisateur créé correspond aux données envoyées
        for key in ['username', 'email', 'first_name', 'last_name']:
            self.assertEqual(response.json[key], self.test_user[key])
        
        # Vérifie que le mot de passe n'est pas renvoyé
        self.assertNotIn('password', response.json)

        # Test GET user spécifique
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        # Vérifie que les données correspondent toujours
        for key in ['username', 'email', 'first_name', 'last_name']:
            self.assertEqual(response.json[key], self.test_user[key])

        # Test LIST users
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        # Vérifie que notre utilisateur est dans la liste
        user_found = False
        for user in response.json:
            if user['id'] == user_id:
                user_found = True
                for key in ['username', 'email', 'first_name', 'last_name']:
                    self.assertEqual(user[key], self.test_user[key])
        self.assertTrue(user_found)

        # Test UPDATE user avec tous les champs requis
        update_data = {
            'username': self.test_user['username'],  # Garde le même username
            'email': self.test_user['email'],        # Garde le même email
            'password': 'GhostBoo123!',              # Mot de passe valide
            'first_name': 'Super',                   # Nouveau prénom
            'last_name': 'Ghost'                     # Nouveau nom
        }
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            headers=self.headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 200)
        # Vérifie que seuls les champs mis à jour ont changé
        self.assertEqual(response.json['first_name'], update_data['first_name'])
        self.assertEqual(response.json['last_name'], update_data['last_name'])
        self.assertEqual(response.json['username'], self.test_user['username'])
        self.assertEqual(response.json['email'], self.test_user['email'])

        # Test GET après UPDATE pour confirmer les changements
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], update_data['first_name'])
        self.assertEqual(response.json['last_name'], update_data['last_name'])
        self.assertEqual(response.json['username'], self.test_user['username'])
        self.assertEqual(response.json['email'], self.test_user['email'])

    def test_place_endpoints(self):
        """Test our haunted places endpoints 🏚️"""
        # Créer un utilisateur d'abord
        user_response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.test_user)
        )
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json['id']

        # Préparer les données de la place avec tous les champs requis
        place_data = self.test_place.copy()
        place_data['owner_id'] = user_id

        # Test CREATE place
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(place_data)
        )
        self.assertEqual(response.status_code, 201)
        place_id = response.json['id']

        # Test UPDATE place
        update_data = {
            'name': 'Haunted Manor',
            'description': 'A very spooky place!',
            'number_rooms': 5,
            'number_bathrooms': 3,
            'max_guest': 10,
            'price_by_night': 150.0,  # Nouveau prix
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': user_id,
            'city': 'Ghost Town',
            'state': 'Haunted State',
            'address': '666 Spooky Lane'
        }
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            headers=self.headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['price_by_night'], 150.0)

    def test_amenity_endpoints(self):
        """Test our supernatural amenities endpoints ✨"""
        # Test CREATE amenity
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.headers,
            data=json.dumps(self.test_amenity)
        )
        self.assertEqual(response.status_code, 201)
        amenity_id = response.json['id']

        # Test GET amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Ghost Detector')

        # Test LIST amenities
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_review_endpoints(self):
        """Test our spectral reviews endpoints 📝"""
        # Create necessary user and place first
        user_response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.test_user)
        )
        user_id = user_response.json['id']
        
        self.test_place['owner_id'] = user_id
        place_response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(self.test_place)
        )
        place_id = place_response.json['id']

        # Prepare review data
        self.test_review['user_id'] = user_id
        self.test_review['place_id'] = place_id

        # Test CREATE review
        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(self.test_review)
        )
        self.assertEqual(response.status_code, 201)
        review_id = response.json['id']

        # Test GET review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Super spooky, loved it!')

        # Test DELETE review (only entity with delete in part 2)
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 204)

    def test_error_handling(self):
        """Test our error handling capabilities 🚫"""
        # Test 404 sur un utilisateur non existant
        response = self.client.get('/api/v1/users/non-existent-id')
        self.assertEqual(response.status_code, 404)

        # Test 400 sur création utilisateur invalide
        invalid_user = {
            'username': f'Invalid_{uuid.uuid4().hex[:8]}',
            'email': 'invalid',  # Email invalide
            'password': 'test',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(invalid_user)
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()