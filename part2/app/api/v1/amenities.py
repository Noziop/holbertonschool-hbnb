from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

ns = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = ns.model('Amenity', {
    'id': fields.String(readonly=True, description='The amenity unique identifier'),
    'name' : fields.String(required=True, description='The amenity name')
    })

@ns.route('/')
class AmenityList(Resource):
    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_model)
    @ns.response(200, 'Amenities found')
    @ns.response(404, 'No amenities found')
    def get(self):
        """List all amenities"""
        try:
            amenities = facade.get_all_amenities()
            if amenities and len(amenities) > 0:
                return amenities
            if not amenities:
                return 'No Amenity found', 404
        except Exception as e:
            ns.abort(500, message=f"An error occurred: {str(e)}")

    @ns.doc('create_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_list_with(amenity_model)
    @ns.response(201, 'Amenity created')
    @ns.response(400, 'Amenity exists with the same name')
    def post(self):
        """Create a new amenity"""
        try:
            amenity = facade.create_amenity(ns.payload), 201
            if amenity:
                return amenity
            ns.abort(400, message="Amenity exists with the same name")
        except ValueError as e:
            ns.abort(400, message=str(e))
        except Exception as e:
            ns.abort(500, message=f"An error occurred: {str(e)}")

@ns.route('/<string:id>')
@ns.param('id', 'The amenity identifier')
class Amenity(Resource):
    @ns.doc('options_amenity')
    def options(self, id):
        '''Handle preflight requests'''
        return '', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    
    @ns.doc('get_amenity')
    def get(self, id):
        """Fetch an amenity given its identifier"""
        return facade.get_amenity(id)

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, id):
        """Update an amenity given its identifier"""
        try:
            print(f"DEBUG Route - Received payload: {ns.payload}")  # Debug
            success, message, amenity = facade.update_amenity(id, ns.payload)
            print(f"DEBUG Route - Update result: success={success}, message={message}, amenity={amenity}")  # Debug
            if success and amenity:
                return amenity
            ns.abort(404, message=message)
        except ValueError as e:
            ns.abort(400, message=str(e))
        except Exception as e:
            ns.abort(500, message=f"An error occurred: {str(e)}")

    @ns.doc('delete_amenity')
    @ns.response(204, 'Amenity deleted')
    @ns.response(404, 'Amenity not found')
    def delete(self, id):
        """Delete an amenity given its identifier"""
        try:
            success, message = facade.delete_amenity(id)
            if success:
                return '', 204
            ns.abort(404, message="Amenity not found")
        except ValueError as e:
            ns.abort(400, message=str(e))
        except Exception as e:
            ns.abort(500, message=f"An error occurred: {str(e)}")