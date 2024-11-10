def test_complex_relationships(client):
    """Test complex relationships between entities! 🕸️"""

    # 1. Créer deux propriétaires
    owners_data = [
        {
            "username": "ghost_landlord",
            "email": "landlord@haunted.com",
            "password": "bOO123!@#",
            "first_name": "Lord",
            "last_name": "Ghost",
            "is_active": True,
            "is_admin": False,
        },
        {
            "username": "spirit_host",
            "email": "host@haunted.com",
            "password": "bOO123!@#",
            "first_name": "Host",
            "last_name": "Spirit",
            "is_active": True,
            "is_admin": False,
        },
    ]
    owner_ids = []
    for owner in owners_data:
        response = client.post("/api/v1/users", json=owner)
        assert response.status_code == 201
        owner_ids.append(response.json["id"])

    # 2. Créer des amenities de différentes catégories
    amenities_data = [
        {
            "name": "Ghost Detector",
            "description": "Detects supernatural presence",
            "category": "supernatural",
        },
        {
            "name": "Spirit Shield",
            "description": "Protects against unwanted spirits",
            "category": "safety",
        },
        {
            "name": "Haunted TV",
            "description": "Shows programs from the other side",
            "category": "entertainment",
        },
    ]
    amenity_ids = []
    for amenity in amenities_data:
        response = client.post("/api/v1/amenities", json=amenity)
        assert response.status_code == 201
        amenity_ids.append(response.json["id"])

    # 3. Chaque propriétaire crée plusieurs places
    places_per_owner = []
    for owner_id in owner_ids:
        places_data = [
            {
                "name": f"Manor of {owner_id[:8]}",
                "description": "A very spooky Victorian mansion",
                "owner_id": owner_id,
                "price_by_night": 100.0,
                "number_rooms": 5,
                "number_bathrooms": 3,
                "max_guest": 10,
                "status": "active",
                "property_type": "house",
            },
            {
                "name": f"Cottage of {owner_id[:8]}",
                "description": "A cozy haunted cottage",
                "owner_id": owner_id,
                "price_by_night": 50.0,
                "number_rooms": 2,
                "number_bathrooms": 1,
                "max_guest": 4,
                "status": "active",
                "property_type": "house",
            },
        ]
        owner_places = []
        for place in places_data:
            response = client.post("/api/v1/places", json=place)
            assert response.status_code == 201
            owner_places.append(response.json["id"])
        places_per_owner.append(owner_places)

    # 4. Ajouter différentes combinaisons d'amenities aux places
    for place_ids in places_per_owner:
        # Premier propriétaire : toutes les amenities
        if place_ids == places_per_owner[0]:
            for place_id in place_ids:
                for amenity_id in amenity_ids:
                    response = client.post(
                        f"/api/v1/places/{place_id}/amenities/{amenity_id}"
                    )
                    assert response.status_code == 201
        # Deuxième propriétaire : seulement safety et entertainment
        else:
            for place_id in place_ids:
                for amenity_id in amenity_ids[1:]:  # Skip supernatural
                    response = client.post(
                        f"/api/v1/places/{place_id}/amenities/{amenity_id}"
                    )
                    assert response.status_code == 201

    # 5. Vérifier les relations via différents endpoints
    # Vérifier les places par propriétaire
    for owner_id in owner_ids:
        response = client.get(f"/api/v1/places?owner_id={owner_id}")
        assert response.status_code == 200
        owner_places = [
            place for place in response.json if place["owner_id"] == owner_id
        ]
        assert len(owner_places) == 2  # Chaque propriétaire a 2 places

    # Vérifier les amenities par place
    for i, place_ids in enumerate(places_per_owner):
        # Pour chaque amenity, vérifier qu'elle est liée aux bonnes places
        for amenity_id in amenity_ids:
            response = client.get(f"/api/v1/amenities/{amenity_id}/places")
            assert response.status_code == 200

            # Filtrer les places qui appartiennent au propriétaire actuel
            owner_places = [
                place for place in response.json if place["owner_id"] == owner_ids[i]
            ]

            # Premier propriétaire : toutes les amenities
            if i == 0:
                assert len(owner_places) == len(
                    place_ids
                ), f"Amenity {amenity_id} should be linked to all places of owner {owner_ids[i]}"
            # Deuxième propriétaire : seulement safety et entertainment
            else:
                if amenity_id == amenity_ids[0]:  # supernatural
                    assert (
                        len(owner_places) == 0
                    ), f"Amenity {amenity_id} should not be linked to places of owner {owner_ids[i]}"
                else:  # safety et entertainment
                    assert len(owner_places) == len(
                        place_ids
                    ), f"Amenity {amenity_id} should be linked to all places of owner {owner_ids[i]}"

    # 6. Vérifier la cascade de suppression
    # Soft delete d'un propriétaire
    response = client.delete(f"/api/v1/users/{owner_ids[0]}")
    assert response.status_code == 204

    # Vérifier que ses places sont masquées
    for place_id in places_per_owner[0]:
        response = client.get(f"/api/v1/places/{place_id}")
        assert response.status_code == 404

    # Vérifier que les amenities existent toujours
    for amenity_id in amenity_ids:
        response = client.get(f"/api/v1/amenities/{amenity_id}")
        assert response.status_code == 200
