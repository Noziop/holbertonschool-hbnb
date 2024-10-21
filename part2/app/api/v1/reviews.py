from flask_restx import Namespace, Resource
from app.services.facade import HBnBFacade

ns = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

@ns.route('/')
class ReviewList(Resource):
    @ns.doc('list_reviews')
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @ns.doc('create_review')
    @ns.expect(review_model)  # Assurez-vous de définir review_model
    def post(self):
        """Create a new review"""
        return facade.create_review(ns.payload), 201

@ns.route('/<string:id>')
@ns.param('id', 'The review identifier')
class Review(Resource):
    @ns.doc('get_review')
    def get(self, id):
        """Fetch a review given its identifier"""
        return facade.get_review(id)

    @ns.doc('update_review')
    @ns.expect(review_model)
    def put(self, id):
        """Update a review given its identifier"""
        return facade.update_review(id, ns.payload)

    @ns.doc('delete_review')
    def delete(self, id):
        """Delete a review given its identifier"""
        facade.delete_review(id)
        return '', 204