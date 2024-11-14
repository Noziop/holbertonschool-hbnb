def test_list_reviews_public(client):
    """Test GET /reviews - Liste publique des reviews 📖"""
    response = client.get("/api/v1/reviews")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_review_valid(client, reviewer, reviewer_headers, test_place):
    """Test POST /reviews - Création d'une review valide ✍️"""
    print("\n=== Debug test_create_review_valid ===")
    print(f"Reviewer ID: {reviewer.id}")
    print(f"Test place ID: {test_place}")

    # Créer une review avec le reviewer (pas le propriétaire)
    review_data = {
        "text": "Super endroit hanté !",
        "rating": 5,
        "place_id": test_place,
        "user_id": reviewer.id,
    }
    print(f"Review data: {review_data}")

    response = client.post(
        "/api/v1/reviews",
        json=review_data,
        headers=reviewer_headers,  # Utiliser les headers du reviewer
    )
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")
    assert response.status_code == 201


def test_create_review_unauthorized(client, test_place):
    """Test POST /reviews - Sans authentification 🚫"""
    review_data = {
        "user_id": "some-id",
        "text": "Review non autorisée",
        "rating": 1,
        "place_id": test_place,
    }
    response = client.post("/api/v1/reviews", json=review_data)
    assert response.status_code == 401


def test_create_review_own_place(client, user_headers, normal_user):
    """Test POST /reviews - Tentative de review sur sa propre place 🏠"""
    # Créer une place d'abord
    place_data = {
        "name": "My Place",
        "description": "My haunted place",
        "number_rooms": 3,
        "number_bathrooms": 2,
        "max_guest": 6,
        "price_by_night": 100.0,
        "owner_id": normal_user.id,
        "status": "active",
        "property_type": "house",
    }
    place_response = client.post(
        "/api/v1/places", json=place_data, headers=user_headers
    )
    place_id = place_response.json["id"]

    # Tenter de créer une review sur sa propre place
    review_data = {
        "text": "Ma place est super !",
        "rating": 5,
        "place_id": place_id,
        "user_id": normal_user.id,
    }
    response = client.post(
        "/api/v1/reviews", json=review_data, headers=user_headers
    )
    assert response.status_code == 403


def test_update_review_owner(client, reviewer, test_place):
    """Test PUT /reviews/<id> - Modification par le propriétaire ✨"""
    from flask_jwt_extended import create_access_token

    print("\n=== Debug test_update_review_owner ===")
    print(f"Reviewer ID: {reviewer.id}")
    print(f"Test place ID: {test_place}")

    # Créer un token pour la création
    create_token = create_access_token(
        identity=reviewer.id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": reviewer.id,
        },
    )
    create_headers = {
        "Authorization": f"Bearer {create_token}",
        "Content-Type": "application/json",
    }

    # Créer une review
    review_data = {
        "text": "Review initiale",
        "rating": 4,
        "place_id": test_place,
        "user_id": reviewer.id,
    }
    print(f"Create review data: {review_data}")

    create_response = client.post(
        "/api/v1/reviews", json=review_data, headers=create_headers
    )
    print(f"Create response: {create_response.json}")
    assert create_response.status_code == 201
    review_id = create_response.json["id"]

    # Créer un nouveau token pour la mise à jour
    update_token = create_access_token(
        identity=reviewer.id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": reviewer.id,
        },
    )
    update_headers = {
        "Authorization": f"Bearer {update_token}",
        "Content-Type": "application/json",
    }

    # Modifier la review
    update_data = {
        "text": "Review modifiée",
        "rating": 5,
        "place_id": test_place,
        "user_id": reviewer.id,
    }
    print(f"Update data: {update_data}")

    response = client.put(
        f"/api/v1/reviews/{review_id}",
        json=update_data,
        headers=update_headers,
    )
    print(f"Update response status: {response.status_code}")
    print(f"Update response data: {response.json}")
    assert response.status_code == 200
    assert response.json["text"] == "Review modifiée"
