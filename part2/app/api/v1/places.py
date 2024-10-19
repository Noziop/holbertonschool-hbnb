from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

ns = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = ns.model('Place', {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'name': fields.String(required=True, description='The place name'),
    'description': fields.String(required=True, description='The place description'),
    'number_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'max_guest': fields.Integer(required=True, description='Maximum number of guests'),
    'price_by_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

@ns.route('/')
class PlaceList(Resource):
    @ns.doc('list_places')
    @ns.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.get_all_places()

    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        return facade.create_place(ns.payload), 201

@ns.route('/<string:place_id>')
@ns.response(404, 'Place not found')
@ns.param('place_id', 'The place identifier')
class Place(Resource):
    @ns.doc('get_place')
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Fetch a place given its identifier"""
        place = facade.get_place(place_id)
        if place:
            return place
        ns.abort(404, message="Place not found")

    @ns.doc('update_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Update a place given its identifier"""
        place = facade.update_place(place_id, ns.payload)
        if place:
            return place
        ns.abort(404, message="Place not found")
