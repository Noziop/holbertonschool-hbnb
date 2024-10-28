# app/tests/test_spooky/test_api/test_reviews_api.py
import pytest
import uuid

@pytest.fixture
def owner(client):
    """Create a place owner! 🏰"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        'username': f'ghost_owner_{unique_id}',
        'email': f'owner_{unique_id}@haunted.com',
        'password': 'Boo123!@#',
        'first_name': 'Ghost',
        'last_name': 'Owner',
        'is_active': True
    }
    response = client.post('/api/v1/users', json=user_data)
    return response.json['id']

@pytest.fixture
def reviewer(client):
    """Create a reviewer! 👻"""
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        'username': f'ghost_reviewer_{unique_id}',
        'email': f'reviewer_{unique_id}@haunted.com',
        'password': 'Boo123!@#',
        'first_name': 'Ghost',
        'last_name': 'Reviewer',
        'is_active': True
    }
    response = client.post('/api/v1/users', json=user_data)
    return response.json['id']

@pytest.fixture
def valid_place(client, owner):
    """Create a valid place for our tests! 🏰"""
    unique_id = str(uuid.uuid4())[:8]
    place_data = {
        'name': f'Review Test House {unique_id}',
        'description': 'Perfect for testing reviews!',
        'owner_id': owner,
        'price_by_night': 100.0,
        'number_rooms': 1,
        'number_bathrooms': 1,
        'max_guest': 2,
        'status': 'active',
        'property_type': 'house'
    }
    response = client.post('/api/v1/places', json=place_data)
    return response.json['id']

def test_create_review_valid(client, reviewer, valid_place):
    """Test creating valid review! ✨"""
    data = {
        'user_id': reviewer,
        'place_id': valid_place,
        'text': 'This place is truly haunted! Loved it!',
        'rating': 5
    }
    response = client.post('/api/v1/reviews', json=data)
    assert response.status_code == 201
    assert response.json['text'] == data['text']
    assert response.json['rating'] == data['rating']

def test_create_review_own_place(client, owner, valid_place):
    """Test creating review for own place! 💀"""
    data = {
        'user_id': owner,
        'place_id': valid_place,
        'text': 'Should not work - own place!',
        'rating': 5
    }
    response = client.post('/api/v1/reviews', json=data)
    assert response.status_code == 400
    assert "own place" in str(response.json['message']).lower()

def test_create_review_invalid_rating(client, reviewer, valid_place):
    """Test creating review with invalid rating! 💀"""
    data = {
        'user_id': reviewer,
        'place_id': valid_place,
        'text': 'Invalid rating test',
        'rating': 6  # Rating invalide (max=5)
    }
    response = client.post('/api/v1/reviews', json=data)
    assert response.status_code == 400

def test_get_review_valid(client, reviewer, valid_place):
    """Test getting existing review! 🔍"""
    # Créer une review
    review_data = {
        'user_id': reviewer,
        'place_id': valid_place,
        'text': 'Great haunted experience!',
        'rating': 4
    }
    create_response = client.post('/api/v1/reviews', json=review_data)
    review_id = create_response.json['id']

    # Récupérer la review
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    assert response.json['text'] == review_data['text']

def test_update_review_valid(client, reviewer, valid_place):
    """Test updating review! 📝"""
    # Créer une review
    review_data = {
        'user_id': reviewer,
        'place_id': valid_place,
        'text': 'Initial review',
        'rating': 3
    }
    create_response = client.post('/api/v1/reviews', json=review_data)
    review_id = create_response.json['id']

    # Mettre à jour avec tous les champs requis
    update_data = {
        'text': 'Updated review text',
        'rating': 4,
        'user_id': reviewer,  # Garder l'user_id
        'place_id': valid_place  # Garder le place_id
    }
    response = client.put(f'/api/v1/reviews/{review_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['text'] == update_data['text']

def test_delete_review(client, reviewer, valid_place):
    """Test deleting review! ⚡"""
    # Créer une review avec un texte assez long
    review_data = {
        'user_id': reviewer,
        'place_id': valid_place,
        'text': 'This is a review that will be deleted soon!',  # Plus de 10 caractères
        'rating': 3
    }
    create_response = client.post('/api/v1/reviews', json=review_data)
    review_id = create_response.json['id']

    # Supprimer
    response = client.delete(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 204

    # Vérifier que la review n'existe plus
    get_response = client.get(f'/api/v1/reviews/{review_id}')
    assert get_response.status_code == 404

def test_create_review_invalid_user(client, valid_place):
    """Test creating review with invalid user! 👻"""
    data = {
        'user_id': 'invalid_user_id',
        'place_id': valid_place,
        'text': 'Should not work',
        'rating': 3
    }
    response = client.post('/api/v1/reviews', json=data)
    assert response.status_code == 400

def test_create_review_invalid_place(client, reviewer):
    """Test creating review with invalid place! 🏚️"""
    data = {
        'user_id': reviewer,
        'place_id': 'invalid_place_id',
        'text': 'Should not work',
        'rating': 3
    }
    response = client.post('/api/v1/reviews', json=data)
    assert response.status_code == 400