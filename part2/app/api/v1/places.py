"""Places API routes - The haunted real estate office! 🏚️"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.utils import *

ns = Namespace('places', validate=True, description='Haunted property operations 👻')
facade = HBnBFacade()

# Modèles Swagger/OpenAPI
place_model = ns.model('Place', {
    'id': fields.String(readonly=True, description='Unique ghost identifier'),
    'name': fields.String(required=True, description='Haunted house name'),
    'description': fields.String(required=True, description='Ghost stories included'),
    'number_rooms': fields.Integer(required=True, description='Haunted rooms count'),
    'number_bathrooms': fields.Integer(required=True, description='Possessed bathrooms'),
    'max_guest': fields.Integer(required=True, description='Maximum spirits allowed'),
    'price_by_night': fields.Float(required=True, description='Price per haunted night'),
    'latitude': fields.Float(required=True, description='Supernatural latitude'),
    'longitude': fields.Float(required=True, description='Spectral longitude'),
    'owner_id': fields.String(required=True, description='Ghost owner ID')
})

@ns.route('/')
class PlaceList(Resource):
    @ns.doc('list_places')
    @ns.marshal_list_with(place_model)
    @ns.doc(params={
        'price_min': {'description': 'Minimum price per night', 'type': 'float'},
        'price_max': {'description': 'Maximum price per night', 'type': 'float'},
        'latitude': {'description': 'Latitude for location-based search', 'type': 'float'},
        'longitude': {'description': 'Longitude for location-based search', 'type': 'float'},
        'radius': {'description': 'Search radius in kilometers', 'type': 'float'}
    })
    def get(self):
        """Browse our haunted catalog! 👻"""
        try:
            # Gestion des filtres
            if 'price_min' in request.args and 'price_max' in request.args:
                places = facade.filter_by_price(
                    float(request.args['price_min']),
                    float(request.args['price_max'])
                )
            elif 'latitude' in request.args and 'longitude' in request.args:
                places = facade.get_places_by_location(
                    float(request.args['latitude']),
                    float(request.args['longitude']),
                    float(request.args.get('radius', 10.0))
                )
            else:
                places = facade.get_all_places()
            
            return places if places else ([], 404)
        except ValueError as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Summon a new haunted property! 🏗️"""
        try:
            place = facade.create_place(ns.payload)
            return place, 201
        except ValueError as e:
            ns.abort(400, f"Invalid haunting parameters: {str(e)}")

@ns.route('/<string:place_id>')
@ns.param('place_id', 'The haunted property identifier')
class Place(Resource):
    @ns.doc('get_place')
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Find a specific haunted house! 🔍"""
        try:
            return facade.get_place(place_id)
        except ValueError:
            ns.abort(404, "This ghost house doesn't exist!")

    @ns.doc('update_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Renovate a haunted property! 🏚️"""
        try:
            return facade.update_place(place_id, ns.payload)
        except ValueError as e:
            ns.abort(400, f"Invalid renovation plans: {str(e)}")

    @ns.doc('delete_place')
    @ns.response(204, 'Ghost house vanished')
    def delete(self, place_id):
        """Exorcise a property from our catalog! ⚡"""
        try:
            if facade.delete_place(place_id):
                return '', 204
            ns.abort(404, "This ghost house is already gone!")
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:place_id>/amenities')
class PlaceAmenities(Resource):
    @ns.doc('get_place_amenities')
    def get(self, place_id):
        """Get all supernatural features of this haunted house! 👻"""
        try:
            return [amenity.to_dict() for amenity in facade.get_place_amenities(place_id)]
        except ValueError as e:
            ns.abort(404, str(e))

    @ns.doc('add_amenity')
    @ns.expect(ns.model('AmenityId', {
        'amenity_id': fields.String(required=True, description='The supernatural feature ID')
    }))
    def post(self, place_id):
        """Add a supernatural feature to this haunted house! ✨"""
        try:
            amenity = facade.add_amenity_to_place(place_id, ns.payload['amenity_id'])
            return amenity.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

    @ns.doc('remove_amenity')
    @ns.expect(ns.model('AmenityId', {
        'amenity_id': fields.String(required=True, description='The supernatural feature to exorcise')
    }))
    def delete(self, place_id):
        """Remove a supernatural feature from this haunted house! ⚡"""
        try:
            facade.remove_amenity_from_place(place_id, ns.payload['amenity_id'])
            return '', 204
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @ns.doc('get_place_reviews')
    def get(self, place_id):
        """Read the ghostly guestbook! 📖"""
        try:
            return [review.to_dict() for review in facade.get_place_reviews(place_id)]
        except ValueError as e:
            ns.abort(404, str(e))

    @ns.doc('add_review')
    @ns.expect(ns.model('Review', {
        'user_id': fields.String(required=True),
        'text': fields.String(required=True),
        'rating': fields.Integer(required=True, min=1, max=5)
    }))
    def post(self, place_id):
        """Add your haunted experience to our guestbook! ✍️"""
        try:
            review_data = {**ns.payload, 'place_id': place_id}
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))