# part3/tests/test_api_routes.py
import pytest
from flask import url_for

def test_public_routes(test_client):
    """Test all public routes 🌍"""
    
    # Documentation routes
    response = test_client.get('/api/v1/')
    assert response.status_code == 200
    
    response = test_client.get('/api/v1/swagger.json')
    assert response.status_code == 200

    # Places - public routes
    response = test_client.get('/api/v1/places')
    assert response.status_code == 200
    
    response = test_client.get('/api/v1/places/nonexistent-id')
    assert response.status_code == 404  # Not found, mais pas 401

    # Reviews - public routes
    response = test_client.get('/api/v1/reviews')
    assert response.status_code == 200
    
    response = test_client.get('/api/v1/reviews/nonexistent-id')
    assert response.status_code == 404  # Not found, mais pas 401

    # Amenities - public routes
    response = test_client.get('/api/v1/amenities')
    assert response.status_code == 200
    
    response = test_client.get('/api/v1/amenities/nonexistent-id')
    assert response.status_code == 404  # Not found, mais pas 401

def test_protected_routes_without_auth(test_client):
    """Test protected routes without authentication 🔒"""
    
    # Places
    response = test_client.post('/api/v1/places', json={
        'name': 'Test Place',
        'description': 'Test Description'
    })
    assert response.status_code == 401
    
    response = test_client.put('/api/v1/places/some-id')
    assert response.status_code == 401

    # Reviews
    response = test_client.post('/api/v1/reviews')
    assert response.status_code == 401
    
    response = test_client.put('/api/v1/reviews/some-id')
    assert response.status_code == 401
    
    response = test_client.delete('/api/v1/reviews/some-id')
    assert response.status_code == 401

    # Users
    response = test_client.put('/api/v1/users/some-id')
    assert response.status_code == 401

def test_protected_routes_with_user_auth(test_client, user_headers):
    """Test protected routes with normal user authentication 👤"""
    
    # Places - création
    response = test_client.post('/api/v1/places', 
        headers=user_headers,
        json={
            'name': 'Test Place',
            'description': 'Test Description',
            'price_by_night': 100
        })
    assert response.status_code in [201, 400]  # 201 si créé, 400 si données invalides

    # Reviews - création
    response = test_client.post('/api/v1/reviews',
        headers=user_headers,
        json={
            'text': 'Test Review',
            'rating': 5,
            'place_id': 'some-place-id'
        })
    assert response.status_code in [201, 400, 404]  # 404 si place n'existe pas

def test_admin_routes_with_user_auth(test_client, user_headers):
    """Test admin routes with normal user authentication 🚫"""
    
    # Users list (admin only)
    response = test_client.get('/api/v1/users', headers=user_headers)
    assert response.status_code == 403

    # Amenities management (admin only)
    response = test_client.post('/api/v1/amenities',
        headers=user_headers,
        json={
            'name': 'Test Amenity',
            'description': 'Test Description'
        })
    assert response.status_code == 403

def test_admin_routes_with_admin_auth(test_client, admin_headers):
    """Test admin routes with admin authentication 👑"""
    
    # Users list
    response = test_client.get('/api/v1/users', headers=admin_headers)
    assert response.status_code == 200

    # Amenities management
    response = test_client.post('/api/v1/amenities',
        headers=admin_headers,
        json={
            'name': 'Test Amenity',
            'description': 'Test Description',
            'category': 'comfort'
        })
    assert response.status_code in [201, 400]  # 201 si créé, 400 si données invalides

def test_owner_only_routes(test_client, user_headers, normal_user):
    """Test owner-only routes 🔐"""
    
    # Créer une place pour tester
    response = test_client.post('/api/v1/places',
        headers=user_headers,
        json={
            'name': 'Test Place',
            'description': 'Test Description',
            'price_by_night': 100
        })
    
    if response.status_code == 201:
        place_id = response.json['id']
        
        # Test modification par le propriétaire
        response = test_client.put(f'/api/v1/places/{place_id}',
            headers=user_headers,
            json={'name': 'Updated Place'})
        assert response.status_code == 200