def test_create_place_invalid_data(client, user_headers):
    """Test POST /places avec des données invalides ⚠️"""
    invalid_data = {
        "name": "A",  # Trop court
        "description": "Short",  # Trop court
        "number_rooms": 0,  # Invalide
        "number_bathrooms": -1,  # Invalide
        "max_guest": 0,  # Invalide
        "price_by_night": -100.0,  # Invalide
        "status": "invalid",  # Status invalide
        "property_type": "invalid",  # Type invalide
    }
    response = client.post(
        "/api/v1/places", json=invalid_data, headers=user_headers
    )
    assert response.status_code == 400


def test_update_place_invalid_data(client, user_headers, test_place):
    """Test PUT /places/<id> avec des données invalides ⚠️"""
    invalid_data = {
        "name": "A",  # Trop court
        "price_by_night": -100.0,  # Invalide
    }
    response = client.put(
        f"/api/v1/places/{test_place}", json=invalid_data, headers=user_headers
    )
    assert response.status_code == 400


def test_get_nonexistent_place(client):
    """Test GET /places/<id> avec un ID inexistant ⚠️"""
    response = client.get("/api/v1/places/nonexistent-id")
    assert response.status_code == 404


def test_update_nonexistent_place(client, user_headers):
    """Test PUT /places/<id> avec un ID inexistant ⚠️"""
    update_data = {
        "place_id": "nonexistent-id",
        "owner_id": "nonexistent-id",
        "name": "Updated Manor",
        "description": "Still haunted",
        "price_by_night": 150.0,
        "number_rooms": 4,
        "number_bathrooms": 3,
        "max_guest": 8,
        "status": "active",
        "property_type": "house",
    }
    response = client.put(
        "/api/v1/places/nonexistent-id", json=update_data, headers=user_headers
    )
    print(response.json["message"])
    assert response.status_code == 404


def test_delete_nonexistent_place(client, admin_headers):
    """Test DELETE /places/<id> avec un ID inexistant ⚠️"""
    print("\n=== Debug test_delete_nonexistent_place ===")
    print(f"Admin headers: {admin_headers}")

    # D'abord vérifier que la place n'existe pas
    get_response = client.get("/api/v1/places/nonexistent-id")
    print(f"GET response status: {get_response.status_code}")
    print(f"GET response data: {get_response.json}")
    assert get_response.status_code == 404

    # Ensuite tenter de la supprimer
    response = client.delete(
        "/api/v1/places/nonexistent-id", headers=admin_headers
    )
    print(f"DELETE response status: {response.status_code}")
    print(f"DELETE response data: {response.json}")

    # Vérifier les claims du token
    from flask_jwt_extended import decode_token

    token = admin_headers["Authorization"].split()[1]
    claims = decode_token(token)
    print(f"Token claims: {claims}")

    assert response.status_code == 404


def test_add_amenity_invalid_data(client, user_headers, test_place):
    """Test POST /places/<id>/amenities avec des données invalides ⚠️"""
    # D'abord vérifier que l'amenity n'existe pas
    invalid_data = {"amenity_id": "nonexistent-id"}

    # Créer un token admin pour vérifier l'existence de l'amenity
    from flask_jwt_extended import create_access_token

    admin_token = create_access_token(
        identity="admin",
        additional_claims={
            "is_admin": True,
            "is_active": True,
            "user_id": "admin",
        },
    )
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }

    response = client.post(
        f"/api/v1/places/{test_place}/amenities",
        json=invalid_data,
        headers=admin_headers,  # Utiliser admin_headers pour éviter le 403
    )
    assert response.status_code == 404


def test_get_place_reviews_nonexistent(client):
    """Test GET /places/<id>/reviews avec un ID inexistant ⚠️"""
    response = client.get("/api/v1/places/nonexistent-id/reviews")
    assert response.status_code == 404
