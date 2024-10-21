from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade

ns = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

@ns.route('/')
class AmenityList(Resource):
    @ns.doc('list_amenities')
    def get(self):
        """List all amenities"""
        return facade.get_all_amenities()

    @ns.doc('create_amenity')
    @ns.expect(amenity_model)  # Assurez-vous de définir amenity_model
    def post(self):
        """Create a new amenity"""
        return facade.create_amenity(ns.payload), 201

@ns.route('/<string:id>')
@ns.param('id', 'The amenity identifier')
class Amenity(Resource):
    @ns.doc('get_amenity')
    def get(self, id):
        """Fetch an amenity given its identifier"""
        return facade.get_amenity(id)

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    def put(self, id):
        """Update an amenity given its identifier"""
        return facade.update_amenity(id, ns.payload)

    @ns.doc('delete_amenity')
    def delete(self, id):
        """Delete an amenity given its identifier"""
        facade.delete_amenity(id)
        return '', 204