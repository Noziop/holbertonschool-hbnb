from flask import Flask
from flask_cors import CORS
from flask_restx import Api
# from app.api.v1.places import ns as places_ns
# from app.api.v1.users import ns as users_ns
# from app.api.v1.amenities import ns as amenities_ns
# from app.api.v1.reviews import ns as reviews_ns

def create_app():
    """Summon our haunted API! 👻"""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    # Appliquer CORS à toute l'app
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Créer l'API avec Swagger UI
    api = Api(
        app,
        version='1.0',
        title='Haunted BnB API 👻',
        description='Where ghosts come to REST! 🏚️',
        doc='/docs'
    )

    # Enregistrer nos namespaces
    # api.add_namespace(places_ns, path='/api/v1/places')
    # api.add_namespace(users_ns, path='/api/v1/users')
    # api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app