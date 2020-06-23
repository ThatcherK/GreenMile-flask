from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from app import db
from app.api.models import Recipient

recipients_blueprint = Blueprint("recipients", __name__)
api = Api(recipients_blueprint)

recipient = api.model(
    "Recipient",
    {
        "id": fields.Integer(readOnly=True),
        "email": fields.String(required=True),
        "name": fields.String(required=True),
        "address": fields.String(required=True),
    },
)


class Recipients(Resource):
    @api.expect(recipient, validate=True)
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"message": "Provide valid auth token"}, 401
        post_data = request.get_json()
        name = post_data.get("name")
        email = post_data.get("email")
        address = post_data.get("address")
        response_object = {}
        recipient = Recipient(name, email, address)
        db.session.add(recipient)
        db.session.commit()
        response_object = {
            "message": f"{email} has been added",
            "recipient": recipient.json(),
        }
        return response_object, 201


api.add_resource(Recipients, "/recipients")
