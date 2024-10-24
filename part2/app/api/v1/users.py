"""Users API routes - Where spirits create their accounts! 👻"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.utils import *

ns = Namespace('users', description='Supernatural user operations 👻')
facade = HBnBFacade()

# Modèle Swagger plus complet
user_model = ns.model('User', {
    'id': fields.String(readonly=True, description='Spectral identifier'),
    'username': fields.String(required=True, description='Ghost name'),
    'email': fields.String(required=True, description='Spirit contact'),
    'password': fields.String(required=True, description='Supernatural secret'),
    'first_name': fields.String(description='First haunting name'),
    'last_name': fields.String(description='Last haunting name'),
    'phone_number': fields.String(description='Ghostly phone'),
    'address': fields.String(description='Haunting address'),
    'postal_code': fields.String(description='Spectral code'),
    'city': fields.String(description='City of haunting'),
    'country': fields.String(description='Realm of existence')
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all spirits in our realm! 👻"""
        return facade.find_users()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Summon a new spirit into existence! 👻"""
        try:
            return facade.create_user(ns.payload), 201
        except ValueError as e:
            ns.abort(400, f"Failed to summon spirit: {str(e)}")

@ns.route('/<string:user_id>')
@ns.param('user_id', 'The spectral identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Find a specific spirit! 🔍"""
        try:
            return facade.get_user(user_id)
        except ValueError as e:
            ns.abort(404, f"Spirit not found: {str(e)}")

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a spirit's manifestation! 🌟"""
        try:
            return facade.update_user(user_id, ns.payload)
        except ValueError as e:
            ns.abort(400, f"Failed to update spirit: {str(e)}")

    @ns.doc('delete_user')
    @ns.response(204, 'Spirit vanished successfully')
    @ns.response(404, 'Spirit already vanished')
    def delete(self, user_id):
        """Banish a spirit from our realm! ⚡"""
        try:
            if facade.delete_user(user_id):
                return '', 204
            ns.abort(404, "Spirit already vanished!")
        except ValueError as e:
            ns.abort(400, str(e))