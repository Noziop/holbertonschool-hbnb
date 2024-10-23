from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, version='1.0', title='HBnB API', description='API for HBnB project')

# Importez les namespaces ici
from .v1.users import ns as users_ns
from .v1.places import ns as places_ns
from .v1.amenities import ns as amenities_ns
#from .v1.reviews import ns as reviews_ns

# Ajoutez les namespaces à l'API
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
#api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')