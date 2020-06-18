from flask import Blueprint,request,jsonify
from flask_restx import Resource,Api,fields
from app import db
from app.api.models import Package

packages_blueprint = Blueprint('packages',__name__)
api = Api(packages_blueprint)

package = api.model('Package', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'supplier_id': fields.Integer(required=True),
    'weight': fields.String(required=True),
    'recipient_id': fields.Integer(required=True)
})
class Packages(Resource):
    @api.expect(package, validate=True)
    def post(self):
        post_data = request.get_json()
        name = post_data.get('name')
        description = post_data.get('description')
        supplier_id = post_data.get('supplier_id')
        weight = post_data.get('weight')
        recipient_id = post_data.get('recipient_id')
        response_object = {}

        db.session.add(Package(name=name,description=description,supplier_id=supplier_id,weight=weight,recipient_id=recipient_id))
        db.session.commit()
        response_object['message'] = f'{name} has been added'
        return response_object,201
    
api.add_resource(Packages,'/packages')