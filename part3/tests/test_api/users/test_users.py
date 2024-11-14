# tests/test_api/users/test_users.py


def test_list_users_admin(client, admin_headers):
    """Test GET /users - Liste des utilisateurs (admin) 👑"""
    response = client.get("/api/v1/users", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_list_users_unauthorized(client, user_headers):
    """Test GET /users - Non admin 🚫"""
    response = client.get("/api/v1/users", headers=user_headers)
    assert response.status_code == 403


def test_create_user_admin(client, admin_headers):
    """Test POST /users - Création d'utilisateur (admin) 👑"""
    data = {
        "username": "test_ghost",
        "email": "test@ghost.com",
        "password": "Ghost123!",
        "first_name": "Test",
        "last_name": "Ghost",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert response.status_code == 201
    assert response.json["username"] == "test_ghost"


def test_create_user_unauthorized(client, user_headers):
    """Test POST /users - Non admin 🚫"""
    data = {
        "username": "test_ghost",
        "email": "test@ghost.com",
        "password": "Ghost123!",
        "first_name": "Test",
        "last_name": "Ghost",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users", json=data, headers=user_headers)
    assert response.status_code == 403


def test_get_user_details(client, user_headers, normal_user):
    """Test GET /users/<id> - Détails d'un utilisateur 👻"""
    response = client.get(
        f"/api/v1/users/{normal_user.id}", headers=user_headers
    )
    assert response.status_code == 200
    assert response.json["id"] == normal_user.id


def test_update_user_owner(client):
    """Test PUT /users/<id> - Modification par le propriétaire ✨"""
    from flask_jwt_extended import create_access_token

    # 1. Créer un utilisateur
    user_data = {
        "username": "test_ghost",
        "email": "test@ghost.com",
        "password": "Ghost123!",
        "first_name": "Test",
        "last_name": "Ghost",
        "is_active": True,
    }

    # Créer l'utilisateur avec un admin token
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

    # Créer l'utilisateur
    create_response = client.post(
        "/api/v1/users", json=user_data, headers=admin_headers
    )
    assert create_response.status_code == 201
    user_id = create_response.json["id"]

    # 2. Créer un token pour cet utilisateur
    user_token = create_access_token(
        identity=user_id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": user_id,
        },
    )
    user_headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
    }

    # 3. Modifier l'utilisateur
    update_data = {
        "username": "test_ghost",
        "email": "test@ghost.com",
        "password": "Ghost123!",
        "first_name": "Updated",
        "last_name": "Ghost",
        "is_active": True,
    }

    response = client.put(
        f"/api/v1/users/{user_id}", json=update_data, headers=user_headers
    )

    # Vérifier le résultat
    assert (
        response.status_code == 200
    ), f"Expected 200 but got {response.status_code}"
    assert (
        response.json["first_name"] == "Updated"
    ), "First name was not updated"

    # Vérifier que la modification a bien été prise en compte
    final_get = client.get(f"/api/v1/users/{user_id}", headers=user_headers)


def test_update_user_not_owner(client, user_headers, other_user):
    """Test PUT /users/<id> - Modification par un autre utilisateur 🚫"""
    print("\n=== Debug test_update_user_not_owner ===")
    print(f"Other user ID: {other_user.id}")
    print(f"Headers: {user_headers}")

    # Vérifier que le token est valide
    from flask_jwt_extended import decode_token

    token = user_headers["Authorization"].split()[1]
    print(f"Token claims: {decode_token(token)}")

    data = {
        "username": other_user.username,
        "email": other_user.email,
        "first_name": "Hacked",
        "last_name": "Ghost",
        "password": "Ghost123!",
        "is_active": True,
    }
    print(f"Request data: {data}")

    response = client.put(
        f"/api/v1/users/{other_user.id}", json=data, headers=user_headers
    )
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")
    assert response.status_code == 403


def test_delete_user_admin(client, admin_headers, normal_user):
    """Test DELETE /users/<id> - Suppression par admin 👑"""
    response = client.delete(
        f"/api/v1/users/{normal_user.id}", headers=admin_headers
    )
    assert response.status_code == 204


# Invalid Cases
def test_create_user_invalid_data(client, admin_headers):
    """Test POST /users avec des données invalides ⚠️"""
    invalid_data = {
        "username": "t",  # Trop court
        "email": "not_an_email",  # Format invalide
        "password": "short",  # Trop court
        "first_name": "",  # Vide
        "last_name": "",  # Vide
        "is_active": True,
    }
    response = client.post(
        "/api/v1/users", json=invalid_data, headers=admin_headers
    )
    assert response.status_code == 400


def test_update_user_invalid_data(client, user_headers, normal_user):
    """Test PUT /users/<id> avec des données invalides ⚠️"""
    invalid_data = {
        "username": "t",  # Trop court
        "email": "not_an_email",  # Format invalide
        "password": "short",  # Trop court
        "first_name": "",  # Vide
        "last_name": "",  # Vide
        "is_active": True,
    }
    response = client.put(
        f"/api/v1/users/{normal_user.id}",
        json=invalid_data,
        headers=user_headers,
    )
    assert response.status_code == 400


def test_get_nonexistent_user(client, user_headers):
    """Test GET /users/<id> avec un ID inexistant ⚠️"""
    response = client.get("/api/v1/users/nonexistent-id", headers=user_headers)
    assert response.status_code == 404


# Edge Cases
def test_create_user_duplicate_email(client, admin_headers, normal_user):
    """Test POST /users avec un email déjà utilisé 🔄"""
    data = {
        "username": "new_ghost",
        "email": normal_user.email,  # Email déjà utilisé
        "password": "Ghost123!",
        "first_name": "Test",
        "last_name": "Ghost",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert response.status_code == 400


def test_update_user_to_admin(client, user_headers, normal_user):
    """Test PUT /users/<id> tentative de devenir admin 👑"""
    data = {
        "username": normal_user.username,
        "email": normal_user.email,
        "password": "Ghost123!",
        "first_name": "Test",
        "last_name": "Ghost",
        "is_active": True,
        "is_admin": True,  # Tentative de devenir admin
    }
    response = client.put(
        f"/api/v1/users/{normal_user.id}", json=data, headers=user_headers
    )
    assert response.status_code == 200
    assert not response.json["is_admin"]  # Vérifie que is_admin n'a pas changé


def test_delete_already_deleted_user(client):
    """Test DELETE /users/<id> sur un utilisateur déjà supprimé 🗑️"""
    from flask_jwt_extended import create_access_token

    print("\n=== Debug test_delete_already_deleted_user ===")

    # 1. Créer un utilisateur à supprimer
    user_data = {
        "username": "ghost_to_delete",
        "email": "ghost@delete.com",
        "password": "Ghost123!",
        "first_name": "Ghost",
        "last_name": "Delete",
        "is_active": True,
    }

    # Créer l'utilisateur avec un admin token
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

    # Créer l'utilisateur
    create_response = client.post(
        "/api/v1/users", json=user_data, headers=admin_headers
    )
    print(f"Create response: {create_response.json}")
    assert create_response.status_code == 201
    user_id = create_response.json["id"]

    # 2. Première suppression
    first_delete_token = create_access_token(
        identity="admin",
        additional_claims={
            "is_admin": True,
            "is_active": True,
            "user_id": "admin",
        },
    )
    first_delete_headers = {
        "Authorization": f"Bearer {first_delete_token}",
        "Content-Type": "application/json",
    }

    response = client.delete(
        f"/api/v1/users/{user_id}", headers=first_delete_headers
    )
    print(f"First delete status: {response.status_code}")
    assert response.status_code == 204

    # 3. Deuxième suppression avec un nouveau token
    second_delete_token = create_access_token(
        identity="admin",
        additional_claims={
            "is_admin": True,
            "is_active": True,
            "user_id": "admin",
        },
    )
    second_delete_headers = {
        "Authorization": f"Bearer {second_delete_token}",
        "Content-Type": "application/json",
    }

    response = client.delete(
        f"/api/v1/users/{user_id}", headers=second_delete_headers
    )
    print(f"Second delete status: {response.status_code}")
    assert response.status_code == 404
