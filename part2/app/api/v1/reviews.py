"""Reviews API routes - The haunted guestbook! 📖"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.utils import *

ns = Namespace('reviews', description='Supernatural feedback operations 👻')
facade = HBnBFacade()

# Modèle Swagger
review_model = ns.model('Review', {
    'id': fields.String(readonly=True, description='Spectral review ID'),
    'place_id': fields.String(required=True, description='Haunted house ID'),
    'user_id': fields.String(required=True, description='Ghost reviewer ID'),
    'text': fields.String(required=True, description='Haunted feedback'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Spooky rating'),
    'created_at': fields.DateTime(readonly=True, description='When the spirit spoke'),
    'updated_at': fields.DateTime(readonly=True, description='Last ghostly edit')
})

@ns.route('/')
class ReviewList(Resource):
    @ns.doc('list_reviews')
    @ns.marshal_list_with(review_model)
    def get(self):
        """Read all ghostly feedback! 👻"""
        try:
            reviews = facade.get_all_reviews()
            return reviews if reviews else ([], 404)
        except ValueError as e:
            ns.abort(400, f"Failed to summon reviews: {str(e)}")

    @ns.doc('create_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Add your haunted experience! ✍️"""
        try:
            return facade.create_review(ns.payload), 201
        except ValueError as e:
            ns.abort(400, f"Failed to write review: {str(e)}")

@ns.route('/<string:review_id>')
@ns.param('review_id', 'The spectral review identifier')
class Review(Resource):
    @ns.doc('get_review')
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Find a specific haunted review! 🔍"""
        try:
            return facade.get_review(review_id)
        except ValueError as e:
            ns.abort(404, f"Review not found: {str(e)}")

    @ns.doc('update_review')
    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        """Update your ghostly feedback! 📝"""
        try:
            return facade.update_review(review_id, ns.payload)
        except ValueError as e:
            ns.abort(400, f"Failed to update review: {str(e)}")

    @ns.doc('delete_review')
    @ns.response(204, 'Review vanished successfully')
    def delete(self, review_id):
        """Make your review disappear! ⚡"""
        try:
            if facade.delete_review(review_id):
                return '', 204
            ns.abort(404, "Review already vanished!")
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/recent')
class RecentReviews(Resource):
    @ns.doc('get_recent_reviews')
    @ns.marshal_list_with(review_model)
    def get(self):
        """Get the freshest haunted tales! 🆕"""
        try:
            return facade.get_recent_reviews(limit=5)
        except ValueError as e:
            ns.abort(400, str(e))