# app/__init__.py
"""Initialize our haunted application! 👻"""
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from app.utils.haunted_logger import setup_logging

def create_app():
    """Summon our haunted API! 👻"""
    # Setup logging first
    setup_logging()
    
    # Create Flask app
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    # Cors configuration for all origins
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # API configuration with swagger
    api = Api(
        app,
        version='1.0',
        title='Haunted BnB API 👻',
        description='Where ghosts come to REST! 🏚️',
        doc='/docs'
    )

    # Namespaces will be added here when ready
    # api.add_namespace(places_ns, path='/api/v1/places')
    # api.add_namespace(users_ns, path='/api/v1/users')
    # api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app