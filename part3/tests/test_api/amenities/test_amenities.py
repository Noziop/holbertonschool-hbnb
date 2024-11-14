def test_list_amenities_public(client):
    """Test GET /amenities - Liste publique des équipements 🏠"""
    response = client.get("/api/v1/amenities")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_amenity_admin(client, admin_headers):
    """Test POST /amenities - Création d'un équipement (admin) 👑"""
    amenity_data = {
        "name": "Ghost Detector",
        "description": "Détecte les présences spectrales",
        "category": "safety",
    }
    response = client.post(
        "/api/v1/amenities", json=amenity_data, headers=admin_headers
    )
    assert response.status_code == 201
    assert response.json["name"] == "Ghost Detector"


def test_create_amenity_unauthorized(client, user_headers):
    """Test POST /amenities - Non admin 🚫"""
    amenity_data = {
        "name": "Ghost Detector",
        "description": "Détecte les présences spectrales",
        "category": "safety",
    }
    response = client.post(
        "/api/v1/amenities", json=amenity_data, headers=user_headers
    )
    print(response.json)
    print(response.status_code)
    print(response.json["message"])
    assert response.status_code == 403


def test_update_amenity_admin(client, admin_headers):
    """Test PUT /amenities/<id> - Modification par admin 👑"""
    # Créer un équipement d'abord
    amenity_data = {
        "name": "Original Detector",
        "description": "Test equipment",
        "category": "safety",
    }
    create_response = client.post(
        "/api/v1/amenities", json=amenity_data, headers=admin_headers
    )
    amenity_id = create_response.json["id"]

    # Modifier l'équipement
    update_data = {
        "name": "Updated Detector",
        "description": "Updated description",
        "category": "safety",
    }
    response = client.put(
        f"/api/v1/amenities/{amenity_id}",
        json=update_data,
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json["name"] == "Updated Detector"


def test_delete_amenity_admin(client, admin_headers):
    """Test DELETE /amenities/<id> - Suppression par admin 👑"""
    # Créer un équipement d'abord
    amenity_data = {
        "name": "Doomed Detector",
        "description": "To be deleted",
        "category": "safety",
    }
    create_response = client.post(
        "/api/v1/amenities", json=amenity_data, headers=admin_headers
    )
    amenity_id = create_response.json["id"]

    # Supprimer l'équipement
    response = client.delete(
        f"/api/v1/amenities/{amenity_id}", headers=admin_headers
    )
    assert response.status_code == 204
