# tests/test_api/places/test_places.py


def test_list_places_public(client):
    """Test GET /places - Route publique 🌍"""
    response = client.get("/api/v1/places")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_place_valid(client, user_headers, normal_user):
    """Test POST /places - Création valide avec authentification 🏗️"""
    data = {
        "name": "Haunted Manor",
        "description": "A very haunted test place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "owner_id": normal_user.id,
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=data, headers=user_headers)
    assert response.status_code == 201
    assert response.json["name"] == "Haunted Manor"
    assert response.json["owner_id"] == normal_user.id


def test_create_place_unauthorized(client):
    """Test POST /places - Sans authentification 🔒"""
    data = {
        "owner_id": "some-id",
        "name": "Haunted Manor",
        "description": "A very haunted test place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=data)
    assert response.status_code == 401


def test_update_place_owner(client, user_headers, normal_user):
    """Test PUT /places/<id> - Modification par le propriétaire 👻"""
    print("\n=== Debug test_update_place_owner ===")
    print(f"Normal user ID: {normal_user.id}")
    print(f"Headers: {user_headers}")

    # Créer une place d'abord
    place_data = {
        "name": "Original Manor",
        "description": "Test place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "owner_id": normal_user.id,
        "status": "active",
        "property_type": "house",
    }
    print(f"\nPlace creation data: {place_data}")

    create_response = client.post(
        "/api/v1/places", json=place_data, headers=user_headers
    )
    print(f"Create response status: {create_response.status_code}")
    print(f"Create response data: {create_response.json}")

    place_id = create_response.json["id"]
    print(f"Created place ID: {place_id}")

    # Modifier la place directement
    update_data = {**place_data, "name": "Updated Manor"}
    response = client.put(
        f"/api/v1/places/{place_id}", json=update_data, headers=user_headers
    )
    print(f"Update response status: {response.status_code}")
    print(f"Update response data: {response.json}")

    assert response.status_code == 200
    assert response.json["name"] == "Updated Manor"


def test_update_place_not_owner(client, user_headers, other_user):
    """Test PUT /places/<id> - Modification par un autre utilisateur 🚫"""
    # Créer une place avec other_user
    place_data = {
        "name": "Other's Manor",
        "description": "Test place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "owner_id": other_user.id,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post(
        "/api/v1/places", json=place_data, headers=user_headers
    )
    place_id = create_response.json["id"]

    # Tenter de modifier avec un autre utilisateur
    update_data = {**place_data, "name": "Hacked Manor"}
    response = client.put(
        f"/api/v1/places/{place_id}", json=update_data, headers=user_headers
    )
    assert response.status_code == 403


def test_delete_place_admin(client, admin_headers, normal_user):
    """Test DELETE /places/<id> - Suppression par admin 👑"""
    # Créer une place
    place_data = {
        "name": "Doomed Manor",
        "description": "Test place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "owner_id": normal_user.id,
        "status": "active",
        "property_type": "house",
    }
    create_response = client.post(
        "/api/v1/places", json=place_data, headers=admin_headers
    )
    place_id = create_response.json["id"]

    # Supprimer la place
    response = client.delete(
        f"/api/v1/places/{place_id}", headers=admin_headers
    )
    assert response.status_code == 204
