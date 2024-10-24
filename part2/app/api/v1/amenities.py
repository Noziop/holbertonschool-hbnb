"""Amenities API routes - Where supernatural features come to life! 👻"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.utils import magic_wand

ns = Namespace('amenities', description='Supernatural feature operations 👻')
facade = HBnBFacade()

# Modèle Swagger amélioré
amenity_model = ns.model('Amenity', {
    'id': fields.String(readonly=True, description='Supernatural feature ID'),
    'name': fields.String(required=True, description='Feature name'),
    'description': fields.String(required=True, description='Spectral details')
})

@ns.route('/')
class AmenityList(Resource):
    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """Browse our catalog of supernatural features! 👻"""
        try:
            amenities = facade.get_all_amenities()
            return amenities if amenities else ([], 404)
        except ValueError as e:
            ns.abort(400, f"Failed to summon features: {str(e)}")

    @ns.doc('create_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Add a new supernatural feature to our catalog! ✨"""
        try:
            return facade.create_amenity(ns.payload), 201
        except ValueError as e:
            ns.abort(400, f"Failed to create feature: {str(e)}")

@ns.route('/<string:amenity_id>')
@ns.param('amenity_id', 'The supernatural feature identifier')
class Amenity(Resource):
    @ns.doc('get_amenity')
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Find a specific supernatural feature! 🔍"""
        try:
            return facade.get_amenity(amenity_id)
        except ValueError as e:
            ns.abort(404, f"Feature not found: {str(e)}")

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Upgrade a supernatural feature! 🌟"""
        try:
            return facade.update_amenity(amenity_id, ns.payload)
        except ValueError as e:
            ns.abort(400, f"Failed to upgrade feature: {str(e)}")

    @ns.doc('delete_amenity')
    @ns.response(204, 'Feature vanished successfully')
    def delete(self, amenity_id):
        """Make a feature disappear! ⚡"""
        try:
            if facade.delete_amenity(amenity_id):
                return '', 204
            ns.abort(404, "Feature already vanished!")
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:amenity_id>/places')
@ns.param('amenity_id', 'The supernatural feature identifier')
class AmenityPlaces(Resource):
    @ns.doc('get_places_with_amenity')
    def get(self, amenity_id):
        """Find all haunted houses with this feature! 🏚️"""
        try:
            places = facade.get_places_with_amenity(amenity_id)
            return [place.to_dict() for place in places]
        except ValueError as e:
            ns.abort(404, f"Feature not found: {str(e)}")