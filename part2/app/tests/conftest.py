# app/tests/conftest.py
"""Test fixtures for our haunted API! 👻"""

import pytest
from app import create_app
from app.persistence.repository import InMemoryRepository as Repository


@pytest.fixture
def app():
    """Create our haunted test app! 🏰"""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def client(app):
    """Create our test client! 👻"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create our CLI test runner! ⚡"""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up after each test! 🧹"""
    # Nettoyer avant le test
    Repository._instances = {}
    Repository._instances_by_type = {}
    yield
    # Nettoyer après le test
    Repository._instances = {}
    Repository._instances_by_type = {}


@pytest.fixture
def empty_repository():
    """Ensure we start with an empty repository! 🧹"""
    Repository.clear_all()
    return Repository
