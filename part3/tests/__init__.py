# tests/__init__.py
"""Configuration for our haunted test suite! 👻"""
import pytest

from app import create_app, db


@pytest.fixture(scope="session")
def app():
    """Create our haunted test app! 🏰"""
    app = create_app("testing")
    return app


@pytest.fixture(scope="session")
def client(app):
    """Create our ghostly test client! 👻"""
    return app.test_client()


@pytest.fixture(scope="function")
def clean_db(app):
    """Clean our haunted database between tests! 🧹"""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()
