"""Initialize our haunted application! 👻"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.utils.haunted_logger import haunted_logger
from config import config

# Preparing our mystical extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name="default"):
    """Summon our haunted API! 👻"""
    # write everything in the Grimoire
    haunted_logger.setup_logging()

    # Initialize our Main Spell
    app = Flask(__name__)

    # Preparing ingredients for our spell
    app.config.from_object(config[config_name])

    # Adding some Dark Magic to make the RECIPES work
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # AnyOne Fool enough to summon us, will enter our realm !
    CORS(
        app,
        resources={
            r"/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
    )

    # Winding Routes 🛤️ to the realm of Haunted BnB
    from app.api import api_bp

    app.register_blueprint(api_bp)

    return app
