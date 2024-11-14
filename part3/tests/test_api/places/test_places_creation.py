# tests/test_api/places/test_places_creation.py
import pytest
from flask import url_for


def test_create_place_valid(client, user_headers, normal_user):
    """Test POST /places avec des cas valides 🏗️"""
    data = {
        "name": "Test Manor",
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
    assert response.json["name"] == "Test Manor"


def test_create_place_invalid(client, user_headers):
    """Test POST /places avec des cas invalides ⚠️"""
    # Données manquantes
    response = client.post(
        "/api/v1/places", json={"name": "Test"}, headers=user_headers
    )
    assert response.status_code == 400

    # Prix négatif
    data = {
        "name": "Test Manor",
        "description": "A haunted place",
        "price_by_night": -100.0,
    }
    response = client.post("/api/v1/places", json=data, headers=user_headers)
    assert response.status_code == 400


def test_create_place_unauthorized(client):
    """Test POST /places sans authentification 🔒"""
    response = client.post(
        "/api/v1/places",
        json={
            "owner_id": "some-id",
            "name": "Test Manor",
            "description": "A very haunted test place",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 100.0,
            "owner_id": "some-id",
            "status": "active",
            "property_type": "house",
        },
    )
    assert response.status_code == 401
