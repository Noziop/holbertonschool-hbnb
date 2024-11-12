# part3/tests/conftest.py
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User

@pytest.fixture(scope='module')
def test_client():
    """Create a test client for Flask app 👻"""
    app = create_app('testing')
    
    with app.test_client() as testing_client:
        with app.app_context():
            # Créer les tables dans une base de données temporaire
            db.create_all()
            
            # Créer un utilisateur admin pour les tests
            admin = User(
                username="admin",
                email="admin@test.com",
                password="Test1234",
                first_name="Admin",
                last_name="Test",
                is_admin=True
            )
            admin.save()
            
            # Créer un utilisateur normal pour les tests
            user = User(
                username="user",
                email="user@test.com",
                password="tesT1234",
                first_name="Normal",
                last_name="Test",
                is_admin=False
            )
            user.save()
            
            yield testing_client
            
            # Nettoyage
            db.session.remove()
            db.drop_all()

@pytest.fixture()
def user_headers():
    """Create auth headers with normal user token 👤"""
    token = create_access_token(
        identity="user@test.com",
        additional_claims={
            "is_admin": False,
            "is_active": True
        }
    )
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture()
def admin_headers():
    """Create auth headers with admin token 👑"""
    token = create_access_token(
        identity="admin@test.com",
        additional_claims={
            "is_admin": True,
            "is_active": True
        }
    )
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture()
def admin_user(test_client):
    """Get the admin user for tests 👑"""
    return User.get_by_email("admin@test.com")

@pytest.fixture()
def normal_user(test_client):
    """Get the normal user for tests 👤"""
    return User.get_by_email("user@test.com")