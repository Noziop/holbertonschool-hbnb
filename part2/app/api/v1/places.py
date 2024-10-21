from flask import request, abort
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
    @ns.param('page', 'Page number', type=int)
    @ns.param('per_page', 'Items per page', type=int)
    def get(self):
        """List all places"""
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        return facade.get_all_places(page=page, per_page=per_page)

    @ns.doc('create_place')
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        try:
            facade.create_place(ns.payload)
            return '', 201
        except ValueError as e:
            abort(400, f"Invalid parameter: {str(e)}")
        except Exception as e:
            abort(500, f"An error occurred: {str(e)}")
    
@ns.route('/search')
class PlaceSearch(Resource):
    @ns.doc('search_places')
    @ns.param('latitude', 'Latitude coordinate', type=float, required=True)
    @ns.param('longitude', 'Longitude coordinate', type=float, required=True)
    @ns.param('radius', 'Search radius in km', type=float, required=True)
    @ns.param('min_price', 'Minimum price', type=float)
    @ns.param('max_price', 'Maximum price', type=float)
    @ns.param('min_rooms', 'Minimum number of rooms', type=int)
    @ns.param('page', 'Page number', type=int, default=1)
    @ns.param('per_page', 'Items per page', type=int, default=10)
    @ns.marshal_with(place_model)
    def get(self):
        """Search for places"""
        try:
            latitude = float(request.args.get('latitude'))
            longitude = float(request.args.get('longitude'))
            radius = float(request.args.get('radius'))
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            
            # Optional parameters
            min_price = request.args.get('min_price')
            max_price = request.args.get('max_price')
            min_rooms = request.args.get('min_rooms')

            results = facade.search_places(
                latitude, longitude, radius, 
                min_price=min_price, max_price=max_price, min_rooms=min_rooms,
                page=page, per_page=per_page
            )

            return {
                'items': results.items,
                'total': results.total,
                'page': results.page,
                'per_page': results.per_page,
                'pages': results.pages
            }
        except ValueError as e:
            abort(400, f"Invalid parameter: {str(e)}")
        except Exception as e:
            abort(500, f"An error occurred: {str(e)}")

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

    @ns.doc('delete_place')
    @ns.response(204, 'Place deleted')
    def delete(self, place_id):
        """Delete a place given its identifier"""
        if facade.delete_place(place_id):
            return '', 204
        ns.abort(404, message="Place not found")

    @ns.route('/<string:place_id>/amenities')
    class PlaceAmenities(Resource):
        @ns.doc('get_place_amenities')
        def get(self, place_id):
            """Get all amenities for a place"""
            if facade.get_amenities_for_place(place_id):
                return facade.get_amenities_for_place(place_id), 200
            ns.abort(404, message="Place not found")
    
    @ns.doc('add_amenity_to_place')
    @ns.expect(ns.model('AmenityId', {'amenity_id': fields.String}))
    def post(self, place_id):
        """Add an amenity to a place"""
        if  facade.add_amenity_to_place(place_id, ns.payload['amenity_id']):
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

api = ns