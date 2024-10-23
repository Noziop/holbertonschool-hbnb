from flask import request, abort
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.utils import *

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
    @ns.response(404, 'No places found')
    def get(self):
        """List all places"""
        try:
            places = facade.get_all_places()
            if places and len(places) > 0:
                return places
            else:
                return [], 404  # Retourne une liste vide avec un code 404
        except Exception as e:
            ns.abort(500, f"An error occurred: {str(e)}")

    @magic_wand(validate_input('place_data', dict), validate_entity('User', 'owner_id'))
    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        try:
            facade.create_place(ns.payload)
            return self, 201
        except ValueError as e:
            abort(400, f"Invalid parameter: {str(e)}")
        except Exception as e:
            abort(500, f"An error occurred: {str(e)}")

@ns.route('/<string:place_id>')
@ns.response(404, 'Place not found')
@ns.param('place_id', 'The place identifier')
class Place(Resource):
    @ns.doc('options_place')  # Changé de 'options_user' à 'options_place'
    def options(self, place_id):
        '''Handle preflight requests'''
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

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

    @ns.doc('delete_place')
    @ns.response(204, 'Place deleted')
    def delete(self, place_id):
        try:
            success, message = facade.delete_place(place_id)
            if success:
                return '', 204
            ns.abort(404, message="Place not found")
        except ValueError as e:
            ns.abort(400, message=str(e))
        except Exception as e:
            ns.abort(500, message=f"An error occurred: {str(e)}")

# Déplacé hors de la classe Place
@ns.route('/<string:place_id>/amenities')
class PlaceAmenities(Resource):
    @ns.doc('get_place_amenities')
    def get(self, place_id):
        """Get all amenities for a place"""
        if facade.get_place_amenities(place_id):
            return facade.get_place_amenities(place_id), 200
        ns.abort(404, message="Place not found")

    @ns.doc('add_amenity_to_place')
    @ns.expect(ns.model('AmenityId', {'amenity_id': fields.String}))
    def post(self, place_id):
        """Add an amenity to a place"""
        if facade.add_amenity_to_place(place_id, ns.payload['amenity_id']):
            return '', 201
        ns.abort(404, message="Place not found")

    @ns.doc('remove_amenity_from_place')
    @ns.expect(ns.model('AmenityId', {'amenity_id': fields.String}))
    def delete(self, place_id):
        """Remove an amenity from a place"""
        if facade.remove_amenity_from_place(place_id, ns.payload['amenity_id']):
            return '', 204
        ns.abort(404, message="Place not found")

@ns.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @ns.doc('get_place_reviews')
    def get(self, place_id):
        """Get all reviews for a place"""
        if facade.get_reviews_for_place(place_id):
            return facade.get_reviews_for_place(place_id), 200
        ns.abort(404, message="Place not found")

# Supprime cette ligne si tu utilises Blueprint
# api = ns