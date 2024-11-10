def test_amenity_lifecycle(client):
    """Test the complete lifecycle of amenities! 🎭"""

    # 1. Créer plusieurs amenities avec différentes catégories
    amenities_data = [
        {
            "name": "Ghost Detector Pro",
            "description": "Professional supernatural detection equipment",
            "category": "supernatural",
        },
        {
            "name": "Haunted Mirror",
            "description": "Shows reflections from the other side",
            "category": "entertainment",
        },
        {
            "name": "Spirit Shield",
            "description": "Protects against unwanted spiritual energy",
            "category": "safety",
        },
        {
            "name": "Phantom Pillow",
            "description": "Self-fluffing pillow for maximum comfort",
            "category": "comfort",
        },
    ]
    amenity_ids = []
    for amenity in amenities_data:
        response = client.post("/api/v1/amenities", json=amenity)
        assert response.status_code == 201
        amenity_ids.append(response.json["id"])

    # 2. Tester le filtrage par catégorie
    response = client.get("/api/v1/amenities?category=supernatural")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Ghost Detector Pro"

    # 3. Mettre à jour une amenity
    update_data = {
        "name": "Super Ghost Detector Pro",
        "description": "Updated professional supernatural detection equipment",
        "category": "supernatural",
    }
    response = client.put(f"/api/v1/amenities/{amenity_ids[0]}", json=update_data)
    assert response.status_code == 200
    assert response.json["name"] == "Super Ghost Detector Pro"

    # 4. Supprimer une amenity
    response = client.delete(f"/api/v1/amenities/{amenity_ids[1]}")
    assert response.status_code == 204

    # Vérifier que l'amenity n'existe plus du tout
    response = client.get(f"/api/v1/amenities/{amenity_ids[1]}")
    assert response.status_code == 404

    # Vérifier qu'elle n'apparaît plus dans la liste
    response = client.get("/api/v1/amenities")
    assert response.status_code == 200
    amenity_names = [a["name"] for a in response.json]
    assert "Haunted Mirror" not in amenity_names

    # 5. Hard delete une amenity
    response = client.delete(f"/api/v1/amenities/{amenity_ids[2]}?hard=true")
    assert response.status_code == 204

    # Vérifier que l'amenity hard deleted n'existe plus
    response = client.get(f"/api/v1/amenities/{amenity_ids[2]}")
    assert response.status_code == 404

    # 6. Tester les validations
    invalid_amenity = {
        "name": "X",  # Trop court
        "description": "Too short",  # Trop court
        "category": "invalid",  # Catégorie invalide
    }
    response = client.post("/api/v1/amenities", json=invalid_amenity)
    assert response.status_code == 400

    # 7. Vérifier qu'on ne peut pas soft delete deux fois
    response = client.delete(f"/api/v1/amenities/{amenity_ids[1]}")
    assert response.status_code == 404
