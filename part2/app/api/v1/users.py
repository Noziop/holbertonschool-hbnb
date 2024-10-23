from flask_restx import Namespace, Resource, fields, abort
from flask import request
from app.services.facade import HBnBFacade
from app.utils import *

ns = Namespace('users', description='User operations')
facade = HBnBFacade()

user_model = ns.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password', attribute='_password')
})


@magic_wand()
@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.get_all_users()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        try:
            return facade.create_user(ns.payload), 201
        except ValueError as e:
            ns.abort(400, message=str(e))



@ns.route('/<string:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class User(Resource):
    @ns.doc('options_user')
    def options(self, user_id):
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        try:
            user = facade.get_user(user_id)
            if user:
                return user
            abort(404, message="User not found")
        except ValueError as e:
            abort(404, message=str(e))

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.response(200, 'User updated successfully')
    @ns.response(404, 'User not found')
    @ns.marshal_with(user_model)
    def put(self, user_id):
        try:
            user = facade.update_user(user_id, ns.payload)
            if user:
                return user
            abort(404, message="User not found")
        except ValueError as e:
            abort(400, message=str(e))

    @ns.doc('delete_user')
    @ns.response(200, 'User deleted successfully')
    @ns.response(404, 'User not found')
    def delete(self, user_id):
        try:
            success, message = facade.delete_user(user_id)
            if success:
                return {'message': message}, 200
            else:
                ns.abort(404, message=message)
        except ValueError as e:
            ns.abort(404, message=str(e))

api = ns