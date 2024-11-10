def test_user_lifecycle_with_soft_delete(client):
    """Test user lifecycle with soft delete! 👻"""

    # 1. Créer un utilisateur
    user_data = {
        "username": "ghost_owner",
        "email": "ghost@haunted.com",
        "password": "bOO123!@#",
        "first_name": "Ghost",
        "last_name": "Owner",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json["id"]

    # 2. Créer des places pour cet utilisateur
    places_data = [
        {
            "name": "Ghost Manor",
            "description": "A haunted Victorian mansion",
            "owner_id": user_id,
            "price_by_night": 100.0,
            "number_rooms": 5,
            "number_bathrooms": 3,
            "max_guest": 10,
            "status": "active",
            "property_type": "house",
        },
        {
            "name": "Spirit Lodge",
            "description": "A cozy haunted cottage",
            "owner_id": user_id,
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

    # 3. Créer un reviewer
    reviewer_data = {
        "username": "ghost_reviewer",
        "email": "reviewer@haunted.com",
        "password": "bOO123!@#",
        "first_name": "Ghost",
        "last_name": "Reviewer",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users", json=reviewer_data)
    assert response.status_code == 201
    reviewer_id = response.json["id"]

    # 4. Le reviewer laisse des reviews
    reviews_data = [
        {
            "user_id": reviewer_id,
            "place_id": place_ids[0],
            "text": "Amazing haunted experience! Will come back!",
            "rating": 5,
        },
        {
            "user_id": reviewer_id,
            "place_id": place_ids[1],
            "text": "Cozy and spooky, perfect weekend getaway!",
            "rating": 4,
        },
    ]
    for review in reviews_data:
        response = client.post("/api/v1/reviews", json=review)
        assert response.status_code == 201

    # 5. Vérifier les places initiales
    response = client.get(f"/api/v1/places?owner_id={user_id}")
    assert response.status_code == 200
    user_places = [place for place in response.json if place["owner_id"] == user_id]
    assert len(user_places) == 2

    # 6. Soft delete de l'utilisateur
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # 7. Vérifier que ses places sont masquées
    response = client.get(f"/api/v1/places?owner_id={user_id}")
    assert response.status_code == 200
    active_places = [
        place
        for place in response.json
        if place["owner_id"] == user_id and place["status"] == "active"
    ]
    assert len(active_places) == 0


def test_place_lifecycle_with_hard_delete(client):
    """Test place lifecycle with hard delete and its impact on reviews! 👻"""

    # 1. Créer un propriétaire et un reviewer
    users_data = [
        {
            "username": "place_owner",
            "email": "owner@haunted.com",
            "password": "bOO123!@#",
            "first_name": "Place",
            "last_name": "Owner",
            "is_active": True,
            "is_admin": False,
        },
        {
            "username": "place_reviewer",
            "email": "place_reviewer@haunted.com",
            "password": "bOO123!@#",
            "first_name": "Place",
            "last_name": "Reviewer",
            "is_active": True,
            "is_admin": False,
        },
    ]
    user_ids = []
    for user in users_data:
        response = client.post("/api/v1/users", json=user)
        assert response.status_code == 201
        user_ids.append(response.json["id"])
    owner_id, reviewer_id = user_ids

    # 2. Créer une place
    place_data = {
        "name": "Haunted Palace",
        "description": "A magnificent haunted palace",
        "owner_id": owner_id,
        "price_by_night": 200.0,
        "number_rooms": 10,
        "number_bathrooms": 5,
        "max_guest": 20,
        "status": "active",
        "property_type": "house",
    }
    response = client.post("/api/v1/places", json=place_data)
    assert response.status_code == 201
    place_id = response.json["id"]

    # 3. Créer une review
    review_data = {
        "user_id": reviewer_id,
        "place_id": place_id,
        "text": "Most haunted palace ever! Amazing experience!",
        "rating": 5,
    }
    response = client.post("/api/v1/reviews", json=review_data)
    assert response.status_code == 201

    # 4. Hard delete de la place
    response = client.delete(f"/api/v1/places/{place_id}?hard=true")
    assert response.status_code == 204

    # 5. Vérifier que la place n'existe plus
    response = client.get(f"/api/v1/places/{place_id}")
    assert response.status_code == 404

    # 6. Vérifier que les reviews ont été supprimées
    response = client.get("/api/v1/reviews")
    assert response.status_code == 200
    reviews = [review for review in response.json if review["place_id"] == place_id]
    assert len(reviews) == 0, "Les reviews devraient être supprimées avec la place"
