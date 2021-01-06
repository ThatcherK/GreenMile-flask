from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from app import db
from app.api.models import Package, User
from app.api.utilities import randomword

packages_blueprint = Blueprint("packages", __name__)
api = Api(packages_blueprint)

package = api.model(
    "Package",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "supplier_id": fields.Integer(required=True),
        "weight": fields.String(required=True),
        "recipient_id": fields.Integer(required=True),
        "status": fields.String(required=True),
        "tracking_code": fields.String(required=True),
    },
)


class Packages(Resource):
    # @api.expect(package, validate=True)
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Provide valid auth token"}, 401
        auth_token = auth_header.split(" ")[1]
        supplier_id = User.decode_auth_token(auth_token)
        tracking_code = randomword(8)
        status = 1
        response_object = {}
        post_data = request.get_json()
        if not post_data:
            response_object["message"] = "Input payload validation failed"
            return response_object, 400
        name = post_data.get("name")
        description = post_data.get("description")
        weight = post_data.get("weight")
        recipient_id = post_data.get("recipient_id")

        package = Package(
            name, description, supplier_id, weight, recipient_id, status, tracking_code
        )
        db.session.add(package)
        db.session.commit()
        response_object = {
            "message": f"{name} has been added",
            "package": package.json(),
        }
        return response_object, 201

    def get(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Provide valid auth token"}, 401
        auth_token = auth_header.split(" ")[1]
        supplier_id = User.decode_auth_token(auth_token)
        packages = Package.query.filter_by(supplier_id=supplier_id).all()
        print(packages)
        return {"packages": [package.json() for package in packages]}, 200


api.add_resource(Packages, "/packages")

