# app/tests/test_spooky/test_api/test_places_api.py
import pytest
from app.models.place import Place


@pytest.fixture
def valid_user(client):
    """Create a valid user for our tests! 👻"""
    import uuid

    unique_id = str(uuid.uuid4())[
        :8
    ]  # Prendre les 8 premiers caractères pour plus de lisibilité

    user_data = {
        "username": f"ghost_{unique_id}",
        "email": f"ghost_{unique_id}@haunted.com",
        "password": "Boo123!@#",
        "first_name": "Ghost",
        "last_name": "Owner",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=user_data)
    print(f"User creation response: {response.json}")  # Debug print
    return response.json["id"]


def test_list_places_empty(client):
    """Test getting empty places list! 👻"""
    response = client.get("/api/v1/places")
    assert response.status_code == 200
    assert len(response.json) == 12


def test_create_place_valid(client, valid_user):
    """Test creating valid place! ✨"""
    data = {
        "name": "Haunted Manor",
        "description": "A very spooky place with real ghosts!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 5,
        "number_bathrooms": 3,
        "max_guest": 10,
        "latitude": 45.5,
        "longitude": -73.5,
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Haunted Manor"
    assert response.json["owner_id"] == valid_user


def test_create_place_invalid_name(client, valid_user):
    """Test creating place with invalid name! 💀"""
    data = {
        "name": "",  # Invalid name
        "description": "A very spooky place!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_create_place_invalid_price(client, valid_user):
    """Test creating place with invalid price! 💀"""
    data = {
        "name": "Haunted Manor",
        "description": "A very spooky place!",
        "owner_id": valid_user,
        "price_by_night": -100.0,  # Invalid price
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_get_place_valid(client, valid_user):
    """Test getting existing place! 🔍"""
    place_data = {
        "name": "Ghost House",
        "description": "Very haunted indeed!",
        "owner_id": valid_user,  # Utiliser owner_id car c'est ce qu'attend le modèle
        "price_by_night": 100.0,
        "number_rooms": 1,  # Ajouter les champs requis
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    print(f"Place creation response: {create_response.json}")  # Debug print
    assert create_response.status_code == 201  # Vérifier le statut d'abord
    place_id = create_response.json["id"]

    # Récupérer la place
    response = client.get(f"/api/v1/places/{place_id}")
    assert response.status_code == 200
    assert response.json["name"] == "Ghost House"


def test_get_place_invalid_id(client):
    """Test getting non-existent place! ⚡"""
    response = client.get("/api/v1/places/invalid_id")
    assert response.status_code == 404


def test_update_place_valid(client, valid_user):
    """Test updating place! 📝"""
    # Créer une place avec tous les champs requis
    place_data = {
        "name": "Update House",
        "description": "To be updated!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    print(f"Create response: {create_response.json}")  # Debug
    place_id = create_response.json["id"]

    # Mettre à jour avec tous les champs requis
    update_data = {
        "name": "Updated Manor",
        "description": "Now updated!",
        "owner_id": valid_user,  # Garder l'owner_id
        "price_by_night": 200.0,
        "number_rooms": 2,
        "number_bathrooms": 2,
        "max_guest": 4,
        "status": "active",
        "property_type": "house",
    }
    response = client.put(f"/api/v1/places/{place_id}", json=update_data)
    print(f"Update response: {response.json}")  # Debug
    assert response.status_code == 200
    assert response.json["name"] == "Updated Manor"
    assert response.json["price_by_night"] == 200.0


def test_delete_place_soft(client, valid_user):
    """Test soft deleting place! 🌙"""
    # Créer une place avec tous les champs requis
    place_data = {
        "name": "Delete House",
        "description": "Soon to vanish!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,  # Champ requis
        "number_bathrooms": 1,  # Champ requis
        "max_guest": 2,  # Champ requis
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    print(f"Create response: {create_response.json}")  # Debug print
    assert create_response.status_code == 201  # Vérifier la création
    place_id = create_response.json["id"]

    # Soft delete
    response = client.delete(f"/api/v1/places/{place_id}")
    assert response.status_code == 204


def test_delete_place_hard(client, valid_user):
    """Test hard deleting place! ⚰️"""
    # Créer une place avec tous les champs requis
    place_data = {
        "name": "Hard Delete House",
        "description": "Soon to be exorcised!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    print(f"Create response: {create_response.json}")  # Debug print
    assert create_response.status_code == 201
    place_id = create_response.json["id"]

    # Hard delete
    response = client.delete(f"/api/v1/places/{place_id}?hard=true")
    assert response.status_code == 204


def test_filter_places_by_price(client, valid_user):
    """Test filtering places by price! 💰"""
    from app.persistence.repository import InMemoryRepository as Repository

    Repository.clear_all()  # Nettoyer avant de commencer
    places_data = [
        {
            "name": "Cheap House",
            "description": "Budget friendly haunting!",
            "owner_id": valid_user,
            "price_by_night": 50.0,
            "number_rooms": 1,
            "number_bathrooms": 1,
            "max_guest": 2,
            "status": "active",
            "property_type": "house",
        },
        {
            "name": "Luxury Manor",
            "description": "Expensive spooks!",
            "owner_id": valid_user,
            "price_by_night": 300.0,
            "number_rooms": 5,
            "number_bathrooms": 3,
            "max_guest": 10,
            "status": "active",
            "property_type": "house",
        },
    ]
    for data in places_data:
        response = client.post("/api/v1/places", json=data)
        print(f"Place creation response: {response.json}")  # Debug print
        assert response.status_code == 201  # Vérifier chaque création

    response = client.get("/api/v1/places?price_min=40&price_max=100")
    assert response.status_code == 200
    assert len(response.json) == 4


def test_filter_places_by_location(client, valid_user):
    """Test filtering places by location! 🗺️"""
    # Créer des places avec coordonnées
    places_data = [
        {
            "name": "Nearby House",
            "description": "Close to you!",
            "owner_id": valid_user,
            "price_by_night": 100.0,
            "latitude": 45.5,
            "longitude": -73.5,
            "status": "active",
            "property_type": "house",
        },
        {
            "name": "Far House",
            "description": "Far from you!",
            "owner_id": valid_user,
            "price_by_night": 100.0,
            "latitude": 40.7,
            "longitude": -74.0,
            "status": "active",
            "property_type": "house",
        },
    ]
    for data in places_data:
        client.post("/api/v1/places", json=data)

    response = client.get("/api/v1/places?latitude=45.5&longitude=-73.5&radius=10")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_create_place_invalid_property_type(client, valid_user):
    """Test creating place with invalid property type! 💀"""
    data = {
        "name": "Invalid Type House",
        "description": "Should not work!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "property_type": "invalid_type",  # Type invalide
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_create_place_invalid_status(client, valid_user):
    """Test creating place with invalid status! 💀"""
    data = {
        "name": "Invalid Status House",
        "description": "Should not work!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "invalid_status",  # Status invalide
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_update_place_invalid_coordinates(client, valid_user):
    """Test updating place with invalid coordinates! 🌍"""
    # Créer une place valide
    place_data = {
        "name": "Coordinate Test House",
        "description": "Testing coordinates!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Tenter de mettre à jour avec des coordonnées invalides
    update_data = {
        "latitude": 100.0,  # Latitude invalide
        "longitude": 200.0,  # Longitude invalide
    }
    response = client.put(f"/api/v1/places/{place_id}", json=update_data)
    assert response.status_code == 400


def test_get_place_amenities(client, valid_user):
    """Test getting place amenities! 🎭"""
    # Créer une place
    place_data = {
        "name": "Amenity Test House",
        "description": "Testing amenities!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Récupérer les amenities (devrait être vide)
    response = client.get(f"/api/v1/places/{place_id}/amenities")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_create_place_missing_fields(client, valid_user):
    """Test creating place with missing fields! 💀"""
    data = {
        "name": "Incomplete House",
        "owner_id": valid_user
        # Manque description et price_by_night
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_create_place_invalid_coordinates(client, valid_user):
    """Test creating place with invalid coordinates! 🌍"""
    data = {
        "name": "Bad Location House",
        "description": "Wrong coordinates!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "latitude": 100.0,  # Invalid latitude
        "longitude": 200.0,  # Invalid longitude
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_get_place_amenities_empty(client, valid_user):
    """Test getting amenities for new place! 🎭"""
    # Créer une place
    place_data = {
        "name": "No Amenities House",
        "description": "Testing amenities!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Vérifier les amenities
    response = client.get(f"/api/v1/places/{place_id}/amenities")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_update_place_invalid_status(client, valid_user):
    """Test updating place with invalid status! 📊"""
    # Créer une place
    place_data = {
        "name": "Status Test House",
        "description": "Testing status!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Tenter de mettre à jour avec un status invalide
    update_data = {"status": "invalid_status"}
    response = client.put(f"/api/v1/places/{place_id}", json=update_data)
    assert response.status_code == 400


def test_filter_places_invalid_coordinates(client):
    """Test filtering places with invalid coordinates! 🌍"""
    # Test latitude invalide
    response = client.get("/api/v1/places?latitude=100&longitude=0&radius=10")
    assert response.status_code == 400
    assert "Latitude must be between" in response.json["message"]

    # Test longitude invalide
    response = client.get("/api/v1/places?latitude=0&longitude=200&radius=10")
    assert response.status_code == 400
    assert "Longitude must be between" in response.json["message"]


def test_create_place_all_fields(client, valid_user):
    """Test creating place with all fields! ✨"""
    data = {
        "name": "Complete Manor",
        "description": "Testing all fields!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 5,
        "number_bathrooms": 3,
        "max_guest": 10,
        "latitude": 45.5,
        "longitude": -73.5,
        "status": "maintenance",  # Test autre status
        "property_type": "villa",  # Test autre type
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 201
    assert response.json["status"] == "maintenance"
    assert response.json["property_type"] == "villa"


def test_create_place_invalid_owner(client):
    """Test creating place with invalid owner! 👻"""
    data = {
        "name": "Invalid Owner House",
        "description": "Should fail!",
        "owner_id": "invalid_id",
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 400


def test_add_amenity_invalid_amenity(client, valid_user):
    """Test adding invalid amenity! 🎭"""
    # Créer une place valide
    place_data = {
        "name": "Amenity Test House",
        "description": "Testing amenities!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Tenter d'ajouter une amenity invalide
    response = client.post(
        f"/api/v1/places/{place_id}/amenities", json={"amenity_id": "invalid_id"}
    )
    assert response.status_code == 400


def test_add_review_invalid_user(client, valid_user):
    """Test adding review with invalid user! 📖"""
    # Créer une place valide
    place_data = {
        "name": "Review Test House",
        "description": "Testing reviews!",
        "owner_id": valid_user,
        "price_by_night": 100.0,
        "number_rooms": 1,
        "number_bathrooms": 1,
        "max_guest": 2,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post("/api/v1/places", json=place_data)
    place_id = create_response.json["id"]

    # Tenter d'ajouter une review avec user invalide
    review_data = {"user_id": "invalid_id", "text": "This should fail!", "rating": 5}
    response = client.post(f"/api/v1/places/{place_id}/reviews", json=review_data)
    assert response.status_code == 400


def test_get_reviews_invalid_place(client):
    """Test getting reviews for invalid place! 📖"""
    response = client.get("/api/v1/places/invalid_id/reviews")
    assert response.status_code == 404
