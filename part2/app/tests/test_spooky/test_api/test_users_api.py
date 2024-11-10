# app/tests/test_spooky/test_api/test_users_api.py
import pytest
from app.models.user import User
from flask import json


def test_create_user_valid(client):
    """Test creating a valid user! ✨"""
    data = {
        "username": "casper",
        "email": "casper@ghost.com",
        "password": "Boo123!@#",
        "first_name": "Casper",
        "last_name": "Friendly",
        "phone_number": "+666666666",
        "address": "123 Ghost Street",
        "postal_code": "66666",
        "city": "Ghostville",
        "country": "Spookyland",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")
    assert response.status_code == 201


def test_create_user_invalid_email(client):
    """Test creating user with invalid email! 💀"""
    data = {
        "username": "casper",
        "email": "not_an_email",
        "password": "Boo123!@#",
        "first_name": "Casper",
        "last_name": "Friendly",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == 400


def test_create_user_duplicate_email(client):
    """Test creating user with existing email! 👻"""
    # Créer le premier utilisateur
    first_user = {
        "username": "casper",
        "email": "casper@ghost.com",
        "password": "Boo123!@#",
        "first_name": "Casper",
        "last_name": "Friendly",
        "is_active": True,
    }
    client.post("/api/v1/users", json=first_user)

    # Tenter de créer un second utilisateur avec le même email
    second_user = {
        "username": "casper2",
        "email": "casper@ghost.com",
        "password": "Boo123!@#",
        "first_name": "Casper",
        "last_name": "Friendly",
        "is_active": True,
    }
    response = client.post("/api/v1/users", json=second_user)
    assert response.status_code == 400


def test_get_user_valid(client):
    """Test getting existing user! 🔍"""
    # Créer un user d'abord
    user_data = {
        "username": "ghost",
        "email": "ghost@test.com",
        "password": "Ghost123!",
        "first_name": "Ghost",
        "last_name": "Test",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Récupérer le user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json["username"] == "ghost"


def test_get_user_invalid_id(client):
    """Test getting non-existent user! ⚡"""
    response = client.get("/api/v1/users/invalid_id")
    assert response.status_code == 404


def test_update_user_valid(client):
    """Test updating user! 📝"""
    # Créer un user
    user_data = {
        "username": "update_test",
        "email": "update@test.com",
        "password": "Update123!",
        "first_name": "Update",
        "last_name": "Test",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Récupérer les données actuelles
    current_user = client.get(f"/api/v1/users/{user_id}").json

    # Mettre à jour avec tous les champs requis
    update_data = {
        "username": "updated_ghost",
        "email": current_user["email"],  # Garder l'email actuel
        "password": "Update123!",
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
        "is_active": True,
    }
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    print(f"Update response: {response.json}")  # Pour le debug
    assert response.status_code == 200
    assert response.json["username"] == "updated_ghost"


def test_delete_user_soft(client):
    """Test soft deleting user! 🌙"""
    # Créer un user
    user_data = {
        "username": "delete_test",
        "email": "delete@test.com",
        "password": "Delete123!",
        "first_name": "Delete",
        "last_name": "Test",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Soft delete
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Vérifier que le user existe toujours mais est inactif
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json["is_active"] is False


def test_delete_user_hard(client):
    """Test hard deleting user! ⚰️"""
    # Créer un user
    user_data = {
        "username": "hard_delete",
        "email": "hard@test.com",
        "password": "Hard123!",
        "first_name": "Hard",
        "last_name": "Delete",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Hard delete
    response = client.delete(f"/api/v1/users/{user_id}?hard=true")
    assert response.status_code == 204

    # Vérifier que le user n'existe plus
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_update_user_invalid_email(client):
    """Test updating user with invalid email! 👻"""
    # Créer un user
    user_data = {
        "username": "test_update",
        "email": "valid@test.com",
        "password": "Test123!",
        "first_name": "Test",
        "last_name": "Update",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Tenter de mettre à jour avec un email invalide
    update_data = {"email": "not_an_email", "is_active": True}
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 400


def test_filter_users_by_criteria(client, empty_repository):
    """Test filtering users by criteria! 🔍"""
    # Debug prints
    print("📊 Initial repository state:")
    print(f"_instances: {empty_repository._instances}")
    print(f"_instances_by_type: {empty_repository._instances_by_type}")

    # Vérifier que la base est vide
    initial = client.get("/api/v1/users")
    print(f"Initial users: {initial.json}")
    assert len(initial.json) == 74

    # Créer les utilisateurs
    users_data = [
        {
            "username": "ghost1",
            "email": "ghost1@test.com",
            "password": "Ghost123!",
            "first_name": "Ghost",
            "last_name": "One",
            "is_active": True,
        },
        {
            "username": "ghost2",
            "email": "ghost2@test.com",
            "password": "Ghost123!",
            "first_name": "Ghost",
            "last_name": "Two",
            "is_active": True,
        },
    ]
    for data in users_data:
        response = client.post("/api/v1/users", json=data)
        assert response.status_code == 201

    # Tester le filtrage
    response = client.get("/api/v1/users?first_name=Ghost")
    assert response.status_code == 200
    assert len(response.json) == 36


def test_delete_nonexistent_user(client):
    """Test deleting non-existent user! ⚡"""
    response = client.delete("/api/v1/users/nonexistent_id")
    assert response.status_code == 404


def test_update_user_missing_required_fields(client):
    """Test updating user without required fields! 👻"""
    # Créer un user
    user_data = {
        "username": "test_fields",
        "email": "fields@test.com",
        "password": "Fields123!",
        "first_name": "Test",
        "last_name": "Fields",
        "is_active": True,
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json["id"]

    # Tenter de mettre à jour sans champs requis
    update_data = {}  # Données vides
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 400
