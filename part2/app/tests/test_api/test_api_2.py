"""API Test Suite - Testing ALL the haunted endpoints! 👻"""

import unittest
import json
import uuid
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    """Test our spooky API endpoints! 🧪"""

    def setUp(self):
        """Prepare our haunted laboratory! 🧪"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        # Créer un utilisateur pour les tests
        uuid_suffix = uuid.uuid4().hex[:6]
        self.test_user = {
            'username': f'Ghost_{uuid_suffix}',
            'email': f'ghost_{uuid_suffix}@haunted.com',
            'password': 'GhostBoo123!',
            'first_name': 'Ghost',
            'last_name': 'Hunter'
        }
        
        # Créer un place pour les tests
        self.test_place = {
            'name': 'Haunted Manor',
            'description': 'A very spooky place!',
            'price_by_night': 100,
            'number_rooms': 5,
            'number_bathrooms': 3,
            'max_guest': 10,
            'latitude': 37.7749,
            'longitude': -122.4194
        }

        # Créer un amenity pour les tests
        self.test_amenity = {
            'name': 'Ghost Detector',
            'description': 'Detects supernatural activity'
        }

        # Créer un review pour les tests
        self.test_review = {
            'text': 'Super spooky, loved it!',
            'rating': 5
        }

    def test_user_edge_cases(self):
        """Test user endpoint edge cases 👻"""
        # Test création utilisateur avec email invalide
        invalid_user = self.test_user.copy()
        invalid_user['email'] = 'not_an_email'
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(invalid_user)
        )
        self.assertEqual(response.status_code, 400)

        # Test création utilisateur avec mot de passe faible
        weak_pass_user = self.test_user.copy()
        weak_pass_user['password'] = 'weak'
        response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(weak_pass_user)
        )
        self.assertEqual(response.status_code, 400)

        # Test mise à jour avec données invalides
        response = self.client.put(
            '/api/v1/users/non-existent-id',
            headers=self.headers,
            data=json.dumps({'email': 'invalid'})
        )
        self.assertEqual(response.status_code, 400)

    def test_place_edge_cases(self):
        """Test place endpoint edge cases 🏚️"""
        # Créer un utilisateur d'abord
        user_response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.test_user)
        )
        user_id = user_response.json['id']
        self.test_place['owner_id'] = user_id

        # Test création place avec prix négatif
        invalid_place = self.test_place.copy()
        invalid_place['price_by_night'] = -100
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(invalid_place)
        )
        self.assertEqual(response.status_code, 400)

        # Test création place avec coordonnées invalides
        invalid_place = self.test_place.copy()
        invalid_place['latitude'] = 200
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(invalid_place)
        )
        self.assertEqual(response.status_code, 400)

        # Créer une place avec Paris comme ville
        valid_place = self.test_place.copy()
        valid_place['city'] = 'Paris'
        valid_place['owner_id'] = user_id
        response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(valid_place)
        )
        self.assertEqual(response.status_code, 201)

        # Test filtrage des places
        response = self.client.get('/api/v1/places/?city=Paris')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_amenity_edge_cases(self):
        """Test amenity endpoint edge cases ✨"""
        # Test création amenity sans nom
        invalid_amenity = {'description': 'No name here'}
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self.headers,
            data=json.dumps(invalid_amenity)
        )
        self.assertEqual(response.status_code, 400)

        # Test mise à jour amenity inexistante
        response = self.client.put(
            '/api/v1/amenities/non-existent-id',
            headers=self.headers,
            data=json.dumps({'name': 'New Name'})
        )
        self.assertEqual(response.status_code, 400)

        # Test liste avec filtres
        response = self.client.get('/api/v1/amenities/?name=Ghost')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_review_edge_cases(self):
        """Test review endpoint edge cases 📝"""
        # Créer place et user pour les tests
        user_response = self.client.post(
            '/api/v1/users/',
            headers=self.headers,
            data=json.dumps(self.test_user)
        )
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json['id']

        self.test_place = {
            'name': 'Haunted Manor',
            'description': 'A very spooky place!',
            'price_by_night': 100.0,
            'number_rooms': 5,
            'number_bathrooms': 3,
            'max_guest': 10,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': user_id,  # Important !
            'city': 'Ghost Town',  # Ajout des champs requis
            'state': 'Haunted State',
            'address': '666 Spooky Lane'
        }

        place_response = self.client.post(
            '/api/v1/places/',
            headers=self.headers,
            data=json.dumps(self.test_place)
        )
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json['id']

        # Créer une review valide d'abord
        valid_review = {
            'text': 'Super spooky place!',
            'rating': 5,
            'user_id': user_id,
            'place_id': place_id
        }
        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(valid_review)
        )
        self.assertEqual(response.status_code, 201)

        # Test création review avec rating invalide
        invalid_review = self.test_review.copy()
        invalid_review.update({
            'user_id': user_id,
            'place_id': place_id,
            'rating': 6  # Rating > 5 devrait échouer
        })
        response = self.client.post(
            '/api/v1/reviews/',
            headers=self.headers,
            data=json.dumps(invalid_review)
        )
        self.assertEqual(response.status_code, 400)

        # Test suppression review inexistante
        response = self.client.delete('/api/v1/reviews/non-existent-id')
        self.assertEqual(response.status_code, 404)

        # Test liste avec filtres
        response = self.client.get(f'/api/v1/reviews/?place_id={place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)