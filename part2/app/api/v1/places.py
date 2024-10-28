# app/api/v1/places.py
"""Places API routes - The haunted real estate office! 🏚️"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.models.amenity import Amenity
from app.models.placeamenity import PlaceAmenity
from app.api import log_me  # Notre décorateur !

ns = Namespace('places', 
    validate=True, 
    description='Haunted property operations 👻',
    path='/api/v1/places'
)
facade = HBnBFacade()

# Modèles Swagger/OpenAPI plus détaillés
place_model = ns.model('Place', {'id': fields.String(readonly=True, description='Unique ghost identifier', example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(required=True, min_length=3, description='Haunted house name', example='Spooky Manor'),
    'description': fields.String(required=True, min_length=10, description='Ghost stories included', example='A very haunted place with mysterious occurrences'),
    'number_rooms': fields.Integer(required=True, min=1, description='Haunted rooms count', example=5),
    'number_bathrooms': fields.Integer(required=True, min=1, description='Possessed bathrooms', example=2),
    'max_guest': fields.Integer(required=True, min=1, description='Maximum spirits allowed', example=4),
    'price_by_night': fields.Float(required=True, min=0.0, description='Price per haunted night', example=100.0),
    'latitude': fields.Float(required=False, min=-90.0, max=90.0, description='Supernatural latitude', example=45.5),
    'longitude': fields.Float(required=False, min=-180.0, max=180.0, description='Spectral longitude', example=-73.5),
    'owner_id': fields.String(required=True, description='Ghost owner ID', example='123e4567-e89b-12d3-a456-426614174000'),
    'status': fields.String(required=False, enum=['active', 'maintenance', 'blocked'], description='Current haunting status', example='active'),
    'property_type': fields.String(required=False, enum=['house', 'apartment', 'villa'], description='Type of haunted property',example='house')
})

# Modèles Swagger pour les réponses
place_amenity_model = ns.model('PlaceAmenity', {
    'id': fields.String(readonly=True, description='Unique feature identifier'),
    'name': fields.String(required=True, description='Feature name'),
    'description': fields.String(required=True, description='Feature description')
})

place_review_model = ns.model('PlaceReview', {
    'id': fields.String(readonly=True, description='Review identifier'),
    'user_id': fields.String(required=True, description='Ghost reviewer ID'),
    'text': fields.String(required=True, min_length=10, description='Haunted feedback'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Spooky rating')
})

@ns.route('/')
class PlaceList(Resource):
    @log_me
    @ns.doc('list_places',
        responses={
            200: 'Success',
            400: 'Invalid parameters',
            404: 'No places found'
        })
    @ns.marshal_list_with(place_model)
    @ns.param('price_min', 'Minimum price per night', type=float)
    @ns.param('price_max', 'Maximum price per night', type=float)
    @ns.param('latitude', 'Latitude for location search', type=float)
    @ns.param('longitude', 'Longitude for location search', type=float)
    @ns.param('radius', 'Search radius in kilometers', type=float, default=10.0)
    def get(self):
        """Browse our haunted catalog! 👻"""
        try:
            # Filtrage par prix
            if 'price_min' in request.args and 'price_max' in request.args:
                min_price = float(request.args['price_min'])
                max_price = float(request.args['price_max'])
                return Place.filter_by_price(min_price, max_price)

            # Recherche par localisation
            if all(k in request.args for k in ['latitude', 'longitude']):
                latitude = float(request.args['latitude'])
                longitude = float(request.args['longitude'])
                
                # Valider les coordonnées
                if not (-90 <= latitude <= 90):
                    raise ValueError("Latitude must be between -90 and 90")
                if not (-180 <= longitude <= 180):
                    raise ValueError("Longitude must be between -180 and 180")
                
                return Place.get_by_location(
                    latitude,
                    longitude,
                    float(request.args.get('radius', 10.0))
                )

            # Liste complète
            return facade.find(Place)

        except ValueError as e:
            ns.abort(400, f"Invalid parameters: {str(e)}")

    @log_me
    @ns.doc('create_place',
        responses={
            201: 'Place created successfully',
            400: 'Invalid input',
            401: 'Unauthorized'
        })
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Summon a new haunted property! 🏗️"""
        try:
            new_place = facade.create(Place, ns.payload)
            return new_place, 201
        except ValueError as e:
            ns.abort(400, f"Invalid haunting parameters: {str(e)}")

@ns.route('/<string:place_id>')
@ns.param('place_id', 'The haunted property identifier')
class PlaceResource(Resource):
    @log_me
    @ns.doc('get_place', responses={200: 'Success', 404: 'Place not found'})
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """Find a specific haunted house! 🔍"""
        try:
            return facade.get(Place, place_id)
        except ValueError:
            ns.abort(404, "This ghost house doesn't exist!")

    @log_me
    @ns.doc('update_place', responses={200: 'Success', 400: 'Invalid parameters', 404: 'Place not found'})
    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """Renovate a haunted property! 🏚️"""
        try:
            return facade.update(Place, place_id, ns.payload)
        except ValueError as e:
            ns.abort(400, f"Invalid renovation plans: {str(e)}")

    @log_me
    @ns.doc('delete_place', responses={204: 'Place deleted', 404: 'Place not found'})
    @ns.param('hard', 'Perform hard delete (permanent)', type=bool, default=False)
    @ns.response(204, 'Ghost house vanished')
    def delete(self, place_id):
        """Exorcise a property! ⚡"""
        try:
            hard = request.args.get('hard', 'false').lower() == 'true'
            if facade.delete(Place, place_id, hard=hard):
                return '', 204
            ns.abort(404, "This ghost house is already gone!")
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:place_id>/amenities')
@ns.param('place_id', 'The haunted property identifier')
class PlaceAmenities(Resource):
    @log_me
    @ns.doc('get_place_amenities', responses={200: 'Success', 404: 'Place not found'})
    @ns.marshal_list_with(place_amenity_model)
    def get(self, place_id):
        """Get all supernatural features! 👻"""
        try:
            facade.get(Place, place_id)
            links = facade.find(PlaceAmenity, place_id=place_id)
            amenities = [facade.get(Amenity, link.amenity_id) for link in links]
            return amenities
        except ValueError as e:
            ns.abort(404, str(e))

    @log_me
    @ns.doc('add_amenity', responses={201: 'Amenity added', 400: 'Invalid parameters', 404: 'Place or Amenity not found'})
    @ns.expect(ns.model('AmenityId', {
        'amenity_id': fields.String(required=True, description='The supernatural feature ID', example='123e4567-e89b-12d3-a456-426614174000')
    }))
    @ns.marshal_with(place_amenity_model, code=201)
    def post(self, place_id):
        """Add a supernatural feature! ✨"""
        try:
            facade.get(Place, place_id)
            amenity_id = ns.payload['amenity_id']
            amenity = facade.get(Amenity, amenity_id)
            facade.link_place_amenity(place_id, amenity_id)
            return amenity, 201
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:place_id>/reviews')
@ns.param('place_id', 'The haunted property identifier')
class PlaceReviews(Resource):
    @log_me
    @ns.doc('get_place_reviews', responses={200: 'Success', 404: 'Place not found'})
    @ns.marshal_list_with(place_review_model)
    def get(self, place_id):
        """Read the ghostly guestbook! 📖"""
        try:
            facade.get(Place, place_id)
            reviews = facade.find(Review, place_id=place_id)
            return reviews
        except ValueError as e:
            ns.abort(404, str(e))

    @log_me
    @ns.doc('add_review', responses={201: 'Review added', 400: 'Invalid parameters', 404: 'Place or User not found'})
    @ns.expect(place_review_model)
    @ns.marshal_with(place_review_model, code=201)
    def post(self, place_id):
        """Add a haunted experience! ✍️"""
        try:
            facade.get(Place, place_id)
            facade.get(User, ns.payload['user_id'])
            review_data = {**ns.payload, 'place_id': place_id}
            return facade.create(Review, review_data), 201
        except ValueError as e:
            ns.abort(400, str(e))