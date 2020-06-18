from flask import Blueprint,request,jsonify
from flask_restx import Resource,Api,fields
from app import db
from app.api.models import Recipient

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
        post_data = request.get_json()
        name = post_data.get('name')
        email = post_data.get('email')
        address = post_data.get('address')
        response_object = {}
        db.session.add(Recipient(name=name,email=email,address=address))
        db.session.commit()
        response_object['message'] = f'{email} has been added'
        return response_object,201
    
api.add_resource(Recipients,'/recipients')