"""Test module for our ghostly User model! 👻"""

import re
import uuid

import pytest

from app import bcrypt, create_app, db
from app.models.user import User


# Fixtures
@pytest.fixture(scope="function")
def app():
    """Create our haunted test app! 🏰"""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def valid_user_data():
    """Valid ghost data for testing! 👻"""
    return {
        "username": f"Casper_{uuid.uuid4().hex[:4]}",
        "email": f"casper_{uuid.uuid4().hex[:4]}@ghost.com",
        "password": "Boo_123!",
        "first_name": "Casper",
        "last_name": "Ghost",
    }


# Test création utilisateur valide
def test_create_valid_user(app, valid_user_data):
    """Test creating a valid ghost! ✨"""
    with app.app_context():
        user = User(**valid_user_data)
        # Vérifier que l'utilisateur est créé avec les bonnes données
        assert user.username == valid_user_data["username"]
        assert user.email == valid_user_data["email"]
        assert bcrypt.check_password_hash(
            user.password_hash, valid_user_data["password"]
        )
        # Vérifier qu'on peut le retrouver en base
        user.save()
        saved_user = User.get_by_attr(username=user.username)
        assert saved_user is not None
        assert saved_user.username == user.username


# Tests validation username
def test_invalid_username_too_short(app, valid_user_data):
    """Test username too short! 👻"""
    with app.app_context():
        valid_user_data["username"] = "Bo"
        with pytest.raises(
            ValueError, match="Username must be at least 3 characters!"
        ):
            User(**valid_user_data)


def test_invalid_username_special_chars(app, valid_user_data):
    """Test username with invalid characters! 👻"""
    with app.app_context():
        valid_user_data["username"] = "Casper@123"
        with pytest.raises(
            ValueError,
            match="Username can only contain letters, numbers, _ and -",
        ):
            User(**valid_user_data)


# Tests validation email
def test_invalid_email_format(app, valid_user_data):
    """Test invalid email format! 📧"""
    with app.app_context():
        valid_user_data["email"] = "not_an_email"
        with pytest.raises(ValueError, match="Invalid email format!"):
            User(**valid_user_data)


def test_duplicate_email(app, valid_user_data):
    """Test duplicate email! 📧"""
    with app.app_context():
        User(**valid_user_data).save()
        with pytest.raises(ValueError, match="Email already in use!"):
            User(**valid_user_data)


# Tests validation password
@pytest.mark.parametrize(
    "password,error",
    [
        ("short", "Password must be at least 8 characters!"),
        (
            "lowercase123",
            "Password must contain at least one uppercase letter!",
        ),
        (
            "UPPERCASE123",
            "Password must contain at least one lowercase letter!",
        ),
        ("NoNumbers!", "Password must contain at least one number!"),
    ],
)
def test_invalid_passwords(app, valid_user_data, password, error):
    """Test various invalid password formats! 🔒"""
    with app.app_context():
        valid_user_data["password"] = password
        with pytest.raises(ValueError, match=error):
            User(**valid_user_data)


# Tests gestion du compte
def test_delete_user(app, valid_user_data):
    """Test deleting an existing user! ⚰️"""
    with app.app_context():
        user = User(**valid_user_data)
        user.save()
        assert user.delete() is True
        assert user.is_active is False
        assert user.is_deleted is True


def test_pause_reactivate_account(app, valid_user_data):
    """Test pausing and reactivating account! 🌙"""
    with app.app_context():
        user = User(**valid_user_data)
        user.save()

        # Test pause
        assert user.pause_account() is True
        assert user.is_active is False

        # Test reactivation
        assert user.reactivate_account() is True
        assert user.is_active is True


def test_cannot_reactivate_deleted_account(app, valid_user_data):
    """Test cannot reactivate deleted account! 💀"""
    with app.app_context():
        user = User(**valid_user_data)
        user.save()
        user.delete()

        with pytest.raises(
            ValueError, match="Cannot reactivate deleted account!"
        ):
            user.reactivate_account()


# Test to_dict
def test_to_dict_excludes_password(app, valid_user_data):
    """Test that to_dict never includes password! 📚"""
    with app.app_context():
        user = User(**valid_user_data)
        user_dict = user.to_dict()

        # Vérifier que les champs sensibles sont exclus
        assert "password" not in user_dict
        assert "password_hash" not in user_dict

        # Vérifier que les autres champs sont présents et corrects
        assert user_dict["username"] == valid_user_data["username"]
        assert user_dict["email"] == valid_user_data["email"]
        assert user_dict["first_name"] == "Casper"
        assert user_dict["last_name"] == "Ghost"


# tests/models/test_user.py


def test_account_lifecycle(app, valid_user_data):
    """Test complete account lifecycle! 🔄"""
    with app.app_context():
        # Création
        user = User(**valid_user_data)
        user.save()
        assert user.is_active is True
        assert user.is_deleted is False

        # Pause
        assert user.pause_account() is True
        assert user.is_active is False
        assert user.is_deleted is False

        # Réactivation
        assert user.reactivate_account() is True
        assert user.is_active is True
        assert user.is_deleted is False

        # Suppression
        assert user.delete() is True
        assert user.is_active is False
        assert user.is_deleted is True


def test_edge_cases_validation():
    """Test all edge cases for User validation! 🎭"""
    with pytest.raises(ValueError):
        # Test invalid emails
        for email in [
            "not.an.email",
            "@ghost.com",
            "casper@",
            "casper@.com",
            "casper@ghost.",
        ]:
            User(
                username="test_ghost",
                email=email,
                password="Boo_123!",
                first_name="Test",
                last_name="Ghost",
            )

        # Test invalid names
        for name in ["", "a", "123", "Name!", "Name@123"]:
            User(
                username="test_ghost",
                email="test@ghost.com",
                password="Boo_123!",
                first_name=name,
                last_name="Ghost",
            )
            User(
                username="test_ghost",
                email="test@ghost.com",
                password="Boo_123!",
                first_name="Test",
                last_name=name,
            )

        # Test invalid usernames
        for username in ["ab", "test@ghost", "test ghost", ""]:
            User(
                username=username,
                email="test@ghost.com",
                password="Boo_123!",
                first_name="Test",
                last_name="Ghost",
            )


def test_password_edge_cases(app, valid_user_data):
    """Test edge cases for password handling! 🔐"""
    with app.app_context():
        # Test password vide
        valid_user_data["password"] = ""
        with pytest.raises(
            ValueError, match="Password must be at least 8 characters!"
        ):
            User(**valid_user_data)

        # Test password avec espaces
        valid_user_data["password"] = "Pass word123"
        user = User(**valid_user_data)
        assert bcrypt.check_password_hash(user.password_hash, "Pass word123")

        # Test très long password
        long_password = "Aa1" + "x" * 100
        valid_user_data["password"] = long_password
        user = User(**valid_user_data)
        assert bcrypt.check_password_hash(user.password_hash, long_password)


def test_multiple_account_operations(app, valid_user_data):
    """Test multiple account operations! 🎭"""
    with app.app_context():
        user = User(**valid_user_data)
        user.save()

        # Test double pause
        assert user.pause_account() is True
        assert user.pause_account() is True  # Devrait toujours retourner True
        assert user.is_active is False

        # Test réactivation après suppression
        user.delete()
        with pytest.raises(
            ValueError, match="Cannot reactivate deleted account!"
        ):
            user.reactivate_account()


def test_repository_operations(app, valid_user_data):
    """Test repository operations! 📚"""
    with app.app_context():
        user = User(**valid_user_data)

        # Test save
        saved_user = user.save()
        assert saved_user.id == user.id

        # Test get_by_attr avec différents paramètres
        found_user = User.get_by_attr(id=user.id)
        assert found_user.id == user.id

        # Test get_all_by_type
        all_users = User.get_all_by_type()
        assert len(all_users) > 0
        assert all(isinstance(u, User) for u in all_users)


def test_update_operations(app, valid_user_data):
    """Test update operations! 📝"""
    with app.app_context():
        user = User(**valid_user_data)
        user.save()

        # Test update avec données valides
        update_data = {"first_name": "Updated-Name"}
        updated_user = user.update(update_data)
        assert updated_user.first_name == "Updated-Name"

        # Test update avec données invalides
        with pytest.raises(ValueError):
            user.update({"id": "new-id"})  # Ne peut pas modifier l'id
