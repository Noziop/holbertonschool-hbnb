import unittest
import json
from flask import Flask
from flask.testing import FlaskClient
from app import create_app
from app.models.basemodel import InMemoryRepository
from app.models.user import User

def create_test_app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5001'
    return app

class TestUserAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_test_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        InMemoryRepository.clear_all()

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['username'], "testuser")
        self.assertNotIn('password', data)

    def test_create_user_duplicate_username(self):
        self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        create_response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        user_id = json.loads(create_response.data)['id']
        
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], "testuser")
        self.assertNotIn('password', data)

    def test_get_nonexistent_user(self):
        response = self.client.get('/api/v1/users/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        create_response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        user_id = json.loads(create_response.data)['id']
        
        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "Updated")
        self.assertEqual(data['last_name'], "Name")
        self.assertNotIn('password', data)

    def test_update_nonexistent_user(self):
        update_data = {"first_name": "Updated"}
        response = self.client.put('/api/v1/users/nonexistent_id', json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_get_all_users_success(self):
        self.client.post('/api/v1/users/', json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
        })
        self.client.post('/api/v1/users/', json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        })
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        for user in data:
            self.assertNotIn('password', user)

    def test_get_all_users_empty(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "invalid_email",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_required_field(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_data(self):
        create_response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        user_id = json.loads(create_response.data)['id']
        
        update_data = {"email": "invalid_email"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_no_changes(self):
        create_response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
        user_id = json.loads(create_response.data)['id']
        
        update_data = {}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], "testuser")

    def test_create_user_long_username(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "a" * 101,  # Assuming max length is 100
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_weak_password(self):
        response = self.client.post('/api/v1/users/', json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()