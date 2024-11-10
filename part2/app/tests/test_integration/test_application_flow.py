# app/tests/test_integration/test_application_flow.py

import pytest


@pytest.fixture
def ghost_owner(client):
    """Create our first ghost owner! 👻"""
    owner_data = {
        "username": "friendly_ghost",
        "email": "casper@haunted.com",
        "password": "bOO123!@#",
        "first_name": "Casper",
        "last_name": "Ghost",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=owner_data)
    return response.json["id"]


@pytest.fixture
def ghost_reviewer(client):  # Ajouter client comme paramètre
    """Create our ghost reviewer! 👻"""
    reviewer_data = {
        "username": "spooky_reviewer",
        "email": "spooky@haunted.com",
        "password": "Review123!@#",
        "first_name": "Spooky",
        "last_name": "Ghost",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users", json=reviewer_data)
    return response.json["id"]


def test_complete_application_flow(client, ghost_owner, ghost_reviewer):
    """Test a complete application flow! 🏰"""

    # 1. Créer des amenities
    amenities_data = [
        {
            "name": "Ghost Detector",
            "description": "Detects supernatural presence in the vicinity",
            "category": "supernatural",
        },
        {
            "name": "Spirit Camera",
            "description": "Captures ethereal manifestations on film",
            "category": "entertainment",
        },
    ]
    amenity_ids = []
    for amenity in amenities_data:
        response = client.post("/api/v1/amenities", json=amenity)
        assert response.status_code == 201
        amenity_ids.append(response.json["id"])

    # 2. Owner crée deux places hantées
    places_data = [
        {
            "name": "Haunted Manor",
            "description": "A very spooky Victorian mansion",
            "owner_id": ghost_owner,
            "price_by_night": 100.0,
            "number_rooms": 5,
            "number_bathrooms": 3,
            "max_guest": 10,
            "status": "active",
            "property_type": "house",
        },
        {
            "name": "Spooky Cottage",
            "description": "A cozy haunted cottage",
            "owner_id": ghost_owner,
            "price_by_night": 50.0,
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "status": "active",
            "property_type": "house",
        },
    ]
    place_ids = []
    for place in places_data:
        response = client.post("/api/v1/places", json=place)
        assert response.status_code == 201
        place_ids.append(response.json["id"])

    # 3. Ajouter des amenities aux places
    for place_id in place_ids:
        for amenity_id in amenity_ids:
            response = client.post(f"/api/v1/places/{place_id}/amenities/{amenity_id}")
            assert response.status_code == 201

    # 4. Reviewer laisse des reviews
    reviews_data = [
        {
            "user_id": ghost_reviewer,
            "place_id": place_ids[0],
            "text": "Amazing haunted experience! The ghost detector worked perfectly!",
            "rating": 5,
        },
        {
            "user_id": ghost_reviewer,
            "place_id": place_ids[1],
            "text": "Cozy and spooky, but the spirit camera needs new batteries.",
            "rating": 4,
        },
    ]
    for review in reviews_data:
        response = client.post("/api/v1/reviews", json=review)
        assert response.status_code == 201

    # 5. Vérifier les reviews via l'endpoint dédié
    for place_id in place_ids:
        response = client.get(f"/api/v1/places/{place_id}/reviews")
        assert response.status_code == 200
        reviews = response.json
        assert len(reviews) > 0
        # Vérifier que les reviews existent avec les bons ratings
        ratings = [review["rating"] for review in reviews]
        if place_id == place_ids[0]:
            assert 5 in ratings, "Rating 5 not found in place reviews"
        else:
            assert 4 in ratings, "Rating 4 not found in place reviews"

    # 6. Vérifier les amenities des places via les amenities
    for amenity_id in amenity_ids:
        response = client.get(f"/api/v1/amenities/{amenity_id}/places")
        assert response.status_code == 200
        places = response.json
        # Vérifier que l'amenity est bien liée à toutes nos places
        place_ids_from_response = [place["id"] for place in places]
        for place_id in place_ids:
            assert (
                place_id in place_ids_from_response
            ), f"Place {place_id} not found in amenity {amenity_id} places"

    # 7. Owner essaie de reviewer sa propre place (doit échouer)
    invalid_review = {
        "user_id": ghost_owner,
        "place_id": place_ids[0],
        "text": "Should not work - reviewing my own place!",
        "rating": 5,
    }
    response = client.post("/api/v1/reviews", json=invalid_review)
    assert response.status_code == 400
