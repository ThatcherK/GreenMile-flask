from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from app import bcrypt, db
from app.api.models import Invited_user, User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "email": fields.String(required=True),
        "name": fields.String(required=True),
        "password": fields.String(required=True),
    },
)
user_login = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "email": fields.String(required=True),
        "name": fields.String(required=False),
        "password": fields.String(required=True),
    },
)


class SignUp(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        name = post_data.get("name")
        email = post_data.get("email")
        password = post_data.get("password")
        invite_code = post_data.get("invite_code")
        response_object = {}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object["message"] = "Sorry, That email already exists."
            return response_object, 400

        invited_user = Invited_user.query.filter_by(
            email=email, invite_code=invite_code
        ).first()
        if invited_user:
            user = User(name, email, password, invited_user.role_id)
            db.session.add(user)
            db.session.commit()
            response_object["message"] = f"{email} was added!"
            return response_object, 201
        else:
            response_object["message"] = "Not authorised"
            return response_object, 401


api.add_resource(SignUp, "/users")


class AllUsers(Resource):
    @api.marshal_with(user)
    def get(self):
        users = User.query.all()
        return users


api.add_resource(AllUsers, "/allusers")


class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user.json(), 200


api.add_resource(Users, "/users/<int:user_id>")


class LogIn(Resource):
    @api.expect(user_login, validate=True)
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        user = User.query.filter_by(email=email).first()
        response_object = {}

        if not bcrypt.check_password_hash(user.password, password):
            response_object["message"] = "Wrong password"
            return response_object, 401
        if not user:
            response_object["message"] = f"{email} does not exist"
            return response_object, 404
        auth_token = user.encode_auth_token(user.id)

        response_object = {
            "status": "success",
            "message": f"{email} was added!",
            "auth_token": auth_token.decode(),
            "user": user.json(),
        }
        return response_object, 200


api.add_resource(LogIn, "/login")
