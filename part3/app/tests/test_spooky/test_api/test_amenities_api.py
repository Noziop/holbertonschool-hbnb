# app/tests/test_spooky/test_api/test_amenities_api.py
import pytest
from app.models.amenity import Amenity

@pytest.fixture
def valid_amenity_data():
    """Create valid amenity data for tests! 🎭"""
    return {
        'name': 'Ghost Detector',
        'description': 'Detects supernatural presence in the vicinity',
        'category': 'supernatural'
    }

def test_list_amenities_empty(client):
    """Test getting empty amenities list! 👻"""
    response = client.get('/api/v1/amenities')
    assert response.status_code == 200
    assert len(response.json) == 0

def test_create_amenity_valid(client, valid_amenity_data):
    """Test creating valid amenity! ✨"""
    response = client.post('/api/v1/amenities', json=valid_amenity_data)
    assert response.status_code == 201
    assert response.json['name'] == valid_amenity_data['name']
    assert response.json['category'] == valid_amenity_data['category']

def test_create_amenity_invalid_category(client, valid_amenity_data):
    """Test creating amenity with invalid category! 💀"""
    data = valid_amenity_data.copy()
    data['category'] = 'invalid_category'
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_get_amenity_valid(client, valid_amenity_data):
    """Test getting existing amenity! 🔍"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Récupérer l'amenity
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    assert response.json['name'] == valid_amenity_data['name']

def test_get_amenity_invalid_id(client):
    """Test getting non-existent amenity! ⚡"""
    response = client.get('/api/v1/amenities/invalid_id')
    assert response.status_code == 404

def test_update_amenity_valid(client, valid_amenity_data):
    """Test updating amenity! 📝"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Mettre à jour
    update_data = {
        'name': 'Updated Detector',
        'description': 'Even better at detecting ghosts!',
        'category': 'supernatural'
    }
    response = client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['name'] == 'Updated Detector'

def test_delete_amenity_soft(client, valid_amenity_data):
    """Test soft deleting amenity! 🌙"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Soft delete
    response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 204

def test_delete_amenity_hard(client, valid_amenity_data):
    """Test hard deleting amenity! ⚰️"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Hard delete
    response = client.delete(f'/api/v1/amenities/{amenity_id}?hard=true')
    assert response.status_code == 204

    # Vérifier que l'amenity n'existe plus
    get_response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert get_response.status_code == 404

def test_filter_amenities_by_category(client, valid_amenity_data):
    """Test filtering amenities by category! 🎭"""
    # Créer plusieurs amenities
    amenities_data = [
        valid_amenity_data,
        {
            'name': 'Comfort Light',
            'description': 'Soothing spectral light',
            'category': 'comfort'
        }
    ]
    for data in amenities_data:
        client.post('/api/v1/amenities', json=data)

    # Filtrer par catégorie
    response = client.get('/api/v1/amenities?category=supernatural')
    assert response.status_code == 200
    assert len(response.json) == 4

def test_create_amenity_invalid_name(client):
    """Test creating amenity with invalid name! 💀"""
    data = {
        'name': '',  # Nom invalide
        'description': 'Should not work!',
        'category': 'supernatural'
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_create_amenity_invalid_description(client):
    """Test creating amenity with invalid description! 💀"""
    data = {
        'name': 'Ghost Detector',
        'description': 'Too short',  # Description trop courte
        'category': 'supernatural'
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_update_amenity_missing_fields(client, valid_amenity_data):
    """Test updating amenity with missing fields! 📝"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Update avec champs manquants
    update_data = {
        'name': 'Updated Detector'  # Manque description
    }
    response = client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
    assert response.status_code == 400

def test_get_places_for_amenity(client, valid_amenity_data):
    """Test getting places for amenity! 🏰"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Récupérer les places (devrait être vide)
    response = client.get(f'/api/v1/amenities/{amenity_id}/places')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 0

def test_delete_amenity_twice(client, valid_amenity_data):
    """Test deleting same amenity twice! ⚰️"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Premier delete
    response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 204

    # Deuxième delete
    response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 404

def test_create_amenity_invalid_category(client):
    """Test creating amenity with invalid category! 💀"""
    data = {
        'name': 'Invalid Category',
        'description': 'This should not work!',
        'category': 'invalid_category'  # Catégorie invalide
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_update_amenity_invalid_data(client, valid_amenity_data):
    """Test updating amenity with invalid data! 📝"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Update avec données invalides
    update_data = {
        'name': '',  # Nom invalide
        'description': 'too short'  # Description trop courte
    }
    response = client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
    assert response.status_code == 400

def test_get_places_with_amenity(client, valid_amenity_data):
    """Test getting places with this amenity! 🏰"""
    # Créer une amenity
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']
    
    # Pour l'instant, pas de places liées
    response = client.get(f'/api/v1/amenities/{amenity_id}/places')
    assert response.status_code == 200
    assert len(response.json) == 0  # Pas encore de places

def test_create_amenity_invalid_category(client):
    """Test creating amenity with invalid category! 💀"""
    data = {
        'name': 'Ghost Detector',
        'description': 'Detects supernatural presence',
        'category': 'invalid_category'  # Catégorie non listée dans l'enum
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_update_amenity_not_found(client):
    """Test updating non-existent amenity! ⚡"""
    data = {
        'name': 'Updated Feature',
        'description': 'This should not work',
        'category': 'supernatural'
    }
    response = client.put('/api/v1/amenities/invalid_id', json=data)
    assert response.status_code == 404

def test_get_places_for_invalid_amenity(client):
    """Test getting places for non-existent amenity! 🏰"""
    response = client.get('/api/v1/amenities/invalid_id/places')
    assert response.status_code == 404

def test_create_amenity_missing_required_fields(client):
    """Test creating amenity without required fields! 💀"""
    # Test sans description
    data = {
        'name': 'Ghost Detector',
        'category': 'supernatural'
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

    # Test sans name
    data = {
        'description': 'Detects supernatural presence',
        'category': 'supernatural'
    }
    response = client.post('/api/v1/amenities', json=data)
    assert response.status_code == 400

def test_update_amenity_invalid_fields(client, valid_amenity_data):
    """Test updating amenity with invalid fields! 📝"""
    # Créer une amenity valide
    create_response = client.post('/api/v1/amenities', json=valid_amenity_data)
    amenity_id = create_response.json['id']

    # Update avec nom trop court
    update_data = {
        'name': 'ab',  # Trop court (min_length=3)
        'description': 'Valid description that is long enough',
        'category': 'supernatural'
    }
    response = client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
    assert response.status_code == 400