# part3/tests/test_api_routes.py
import pytest
from flask import url_for


def test_public_routes(client):
    """Test all public routes 🌍"""
    # Documentation routes
    response = client.get("/api/v1/")
    assert response.status_code == 200

    response = client.get("/api/v1/swagger.json")
    assert response.status_code == 200

    # Places - public routes
    response = client.get("/api/v1/places")
    assert response.status_code == 200

    # Amenities - public routes
    response = client.get("/api/v1/amenities")
    assert response.status_code == 200


def test_protected_routes_without_auth(client):
    """Test protected routes without authentication 🔒"""
    # Places
    response = client.post(
        "/api/v1/places",
        json={
            "name": "Test Place",
            "description": "Test Description",
            "price_by_night": 100.0,
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "property_type": "apartment",
            "owner_id": "some-id",  # Ajouté
            "status": "active",  # Ajouté
        },
    )
    assert response.status_code == 401

    # Reviews
    response = client.post(
        "/api/v1/reviews",
        json={
            "text": "Test review",
            "rating": 5,
            "place_id": "some-id",
            "user_id": "some-user-id",  # Ajouté
        },
    )
    assert response.status_code == 401


def test_protected_routes_with_user_auth(client, user_headers, normal_user):
    """Test protected routes with normal user authentication 👤"""
    # Places - création
    response = client.post(
        "/api/v1/places",
        headers=user_headers,
        json={
            "name": "Test Place",
            "description": "Test Description",
            "price_by_night": 100.0,
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "property_type": "apartment",
            "owner_id": normal_user.id,  # Utiliser l'ID du normal_user
            "status": "active",
        },
    )
    assert response.status_code in [201, 400]


def test_admin_routes_with_user_auth(client, user_headers):
    """Test admin routes with normal user authentication 🚫"""
    # Users list (admin only)
    response = client.get("/api/v1/users", headers=user_headers)
    assert response.status_code == 403

    # Amenities management (admin only)
    response = client.post(
        "/api/v1/amenities",
        headers=user_headers,
        json={
            "name": "Test Amenity",
            "description": "Test Description",
            "category": "comfort",
        },
    )
    assert response.status_code == 403


def test_admin_routes_with_admin_auth(client, admin_headers):
    """Test admin routes with admin authentication 👑"""
    # Users list
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200

    # Amenities management
    response = client.post(
        "/api/v1/amenities",
        headers=admin_headers,
        json={
            "name": "Test Amenity",
            "description": "Test Description",
            "category": "comfort",
        },
    )
    assert response.status_code in [201, 400]


def test_owner_only_routes(client, user_headers, normal_user):
    """Test owner-only routes 🔐"""
    print("\n=== Test owner_only_routes ===")
    print(f"Normal user ID: {normal_user.id}")
    print(f"Headers: {user_headers}")

    # Créer une place pour tester
    response = client.post(
        "/api/v1/places",
        headers=user_headers,
        json={
            "name": "Test Place",
            "description": "Test Description",
            "price_by_night": 100.0,
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "property_type": "apartment",
            "owner_id": normal_user.id,
            "status": "active",
        },
    )
    print(f"\nPOST Response status: {response.status_code}")
    print(f"POST Response data: {response.json}")

    if response.status_code == 201:
        place_id = response.json["id"]
        print(f"\nCreated place ID: {place_id}")

        # Test modification par le propriétaire
        put_response = client.put(
            f"/api/v1/places/{place_id}",
            headers=user_headers,
            json={
                "name": "update Test Place",
                "description": "Test Description",
                "price_by_night": 100.0,
                "number_rooms": 2,
                "number_bathrooms": 1,
                "max_guest": 4,
                "property_type": "apartment",
                "owner_id": normal_user.id,
                "status": "active",
            },
        )
        print(f"\nPUT Response status: {put_response.status_code}")
        print(f"PUT Response data: {put_response.json}")
        assert put_response.status_code == 200
