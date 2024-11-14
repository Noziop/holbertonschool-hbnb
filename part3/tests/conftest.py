# tests/conftest.py
import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User


@pytest.fixture()
def app():
    """Create test Flask app! 🎭"""
    app = create_app("testing")
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Create test client! 🧪"""
    return app.test_client()


@pytest.fixture()
def admin_user(app):
    """Create admin user! 👑"""
    admin = User(
        username="admin",
        email="admin@test.com",
        password="Admin123!",
        first_name="Admin",
        last_name="Ghost",
        is_admin=True,
        is_active=True,
    ).save()
    return admin


@pytest.fixture()
def normal_user(app):
    """Create normal user! 👤"""
    user = User(
        username="user",
        email="user@test.com",
        password="User123!",
        first_name="Normal",
        last_name="Ghost",
        is_admin=False,
        is_active=True,
    ).save()
    return user


@pytest.fixture()
def admin_token(admin_user):
    """Create admin token! 👑"""
    return create_access_token(
        identity=admin_user.id,
        additional_claims={
            "is_admin": True,
            "is_active": True,
            "user_id": admin_user.id,
        },
    )


@pytest.fixture()
def admin_headers(admin_token):
    """Create admin headers! 👑"""
    return {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture()
def user_token(normal_user):
    """Create user token! 👤"""
    return create_access_token(
        identity=normal_user.id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": normal_user.id,
        },
    )


@pytest.fixture()
def user_headers(client, normal_user):
    """Create auth headers with normal user token 👤"""
    with client.application.app_context():
        token = create_access_token(
            identity=normal_user.id,
            additional_claims={
                "is_admin": False,
                "is_active": True,
                "user_id": normal_user.id,
            },
        )
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }


@pytest.fixture()
def other_user(app):
    """Create another user for testing! 👻"""
    user = User(
        username="other_user",
        email="other@test.com",
        password="Other123!",
        first_name="Other",
        last_name="Ghost",
        is_admin=False,
        is_active=True,
    ).save()
    return user


@pytest.fixture()
def other_user_headers(client, other_user):
    """Create auth headers for other user 👤"""
    with client.application.app_context():
        token = create_access_token(
            identity=other_user.id,
            additional_claims={
                "is_admin": False,
                "is_active": True,
                "user_id": other_user.id,
            },
        )
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }


@pytest.fixture
def test_place(client, user_headers, normal_user):
    """Create a test place for amenity tests! 🏰"""
    # Utiliser les mêmes user_headers que ceux qui seront utilisés pour les tests
    place_data = {
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
    response = client.post(
        "/api/v1/places", json=place_data, headers=user_headers
    )
    assert response.status_code == 201  # S'assurer que la création a réussi
    return response.json["id"]


@pytest.fixture
def reviewer(app):
    """Create a reviewer user! 👻"""
    user = User(
        username="reviewer",
        email="reviewer@test.com",
        password="Review123!",
        first_name="Review",
        last_name="Ghost",
        is_admin=False,
        is_active=True,
    ).save()
    return user


@pytest.fixture
def reviewer_headers(client, reviewer):
    """Create headers for reviewer! 👻"""
    token = create_access_token(
        identity=reviewer.id,
        additional_claims={
            "is_admin": False,
            "is_active": True,
            "user_id": reviewer.id,
        },
    )
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def test_user(app):
    """Create a test user for auth tests! 👻"""
    with app.app_context():
        user_data = {
            "username": "test_ghost",
            "email": "test@ghost.com",
            "password": "Ghost123!",
            "first_name": "Test",
            "last_name": "Ghost",
            "is_active": True,
        }
        user = User(**user_data)
        user.save()
        return user_data  # Retourner les données pour les tests
