"""Configuration for our haunted application! 👻"""

import os
from datetime import timedelta


class Config:
    """Hold the configuration for our haunted application! 👻"""

    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_haunted_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "jwt_super_secret_haunted_key"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    BCRYPT_LOG_ROUNDS = 12


class DevelopmentConfig(Config):
    """The anti-chamber of our haunted application! 🚪"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///hbnb_dev.db"
    )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    # Utilisons une base en mémoire pour les tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = True


class ProductionConfig(Config):
    """Now that we have tested our spells, we can cast them! 🧙‍♂️"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
