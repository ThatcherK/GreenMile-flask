from uuid import uuid4
from flask import Blueprint, jsonify, request, current_app
from flask_restx import Api, Resource, fields

from app import db
from app.api.models import Invited_user
from app.api.utilities import send_invite_email

invited_users_blueprint = Blueprint("invited_users", __name__)
api = Api(invited_users_blueprint)

invited_user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "email": fields.String(required=True),
        # "invite_code": fields.String(required=True),
        "role_id": fields.Integer(required=True),
    },
)


class Add_invited_user(Resource):
    @api.expect(invited_user, validate=True)
    def post(self):
        post_data = request.get_json()
        print(post_data)
        email = post_data.get("email")
        role_id = post_data.get("role_id")
        invite_code = str(uuid4())
        response_object = {}

        user = Invited_user.query.filter_by(email=email).first()
        if user:
            response_object["message"] = "Sorry, That email already exists."
            return response_object, 400
        
        invited_user = Invited_user(email=email, invite_code=invite_code, role_id=role_id)
        invited_user.save()
        if current_app.config != "testing":
            send_invite_email(invite_code, invited_user.email, "http://localhost:3000/")
        response_object = {
            "message": f"{email} was added",
            "invited_user": invited_user.json()
            }
        return response_object, 201

    def get(self):
        invited_users = Invited_user.query.all()
        return jsonify({"invited_users": [user.json() for user in invited_users]}), 200


api.add_resource(Add_invited_user, "/invited_user")
