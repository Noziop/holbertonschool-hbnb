# tests/test_api/places/test_places_amenities.py


def test_list_place_amenities_valid(client):
    """Test GET /places/<id>/amenities - Liste des équipements d'une place 🏰"""
    response = client.get("/api/v1/places/some-id/amenities")
    assert response.status_code == 404  # Place non trouvée


def test_add_amenity_to_place_valid(client, user_headers, normal_user):
    """Test POST /places/<id>/amenities - Ajout d'un équipement par le propriétaire ✨"""
    # Créer une place d'abord
    place_data = {
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
    create_response = client.post(
        "/api/v1/places", json=place_data, headers=user_headers
    )
    assert create_response.status_code == 201
    place_id = create_response.json["id"]

    # Ajouter un équipement
    amenity_data = {"amenity_id": "some-amenity-id"}
    response = client.post(
        f"/api/v1/places/{place_id}/amenities",
        json=amenity_data,
        headers=user_headers,
    )
    assert response.status_code == 404  # Amenity non trouvée


def test_add_amenity_unauthorized(client, test_place):
    """Test POST /places/<id>/amenities - Sans authentification 🔒"""
    amenity_data = {"amenity_id": "some-amenity-id"}
    response = client.post(
        f"/api/v1/places/{test_place}/amenities", json=amenity_data
    )
    print(f"\n=== Debug test_add_amenity_unauthorized ===")
    print(f"Place ID: {test_place}")
    print(f"Request data: {amenity_data}")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 401


def test_add_amenity_not_owner(client, user_headers, other_user):
    """Test POST /places/<id>/amenities - Par un non propriétaire 🚫"""
    # Créer une place avec other_user
    from flask_jwt_extended import create_access_token

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

    # Créer la place avec les droits de other_user
    other_token = create_access_token(
        identity=other_user.id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": other_user.id,
        },
    )
    other_headers = {
        "Authorization": f"Bearer {other_token}",
        "Content-Type": "application/json",
    }

    create_response = client.post(
        "/api/v1/places", json=place_data, headers=other_headers
    )
    assert create_response.status_code == 201
    place_id = create_response.json["id"]

    # Tenter d'ajouter un équipement avec un autre utilisateur
    amenity_data = {"amenity_id": "some-amenity-id"}
    response = client.post(
        f"/api/v1/places/{place_id}/amenities",
        json=amenity_data,
        headers=user_headers,
    )
    assert response.status_code == 403
