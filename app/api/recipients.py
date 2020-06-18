from flask import Blueprint,request,jsonify
from flask_restx import Resource,Api,fields
from app import db
from app.api.models import Recipient,User

recipients_blueprint = Blueprint('recipients',__name__)
api = Api(recipients_blueprint)

recipient = api.model('Recipient', {
    'id': fields.Integer(readOnly=True),
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'address': fields.String(required=True)
})

class Recipients(Resource):
    @api.expect(recipient, validate=True)
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'Provide valid auth token'},401
        auth_token = auth_header.split(" ")[1]
        supplier_id = User.decode_auth_token(auth_token)
        post_data = request.get_json()
        name = post_data.get('name')
        email = post_data.get('email')
        address = post_data.get('address')
        response_object = {}
        recipient = Recipient(name,email,address)
        db.session.add(recipient)
        db.session.commit()
        response_object = {
            'message':f'{email} has been added',
            # 'supplier_id':supplier_id,
            'recipient':recipient.json()
            }
        return response_object,201
    
api.add_resource(Recipients,'/recipients')