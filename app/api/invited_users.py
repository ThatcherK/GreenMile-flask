from flask import Blueprint,request,jsonify
from flask_restx import Resource,Api,fields
from app import db
from app.api.models import Invited_user

invited_users_blueprint = Blueprint('invited_users',__name__)
api = Api(users_blueprint)

class Create_invite(Resource):
    def post (self):
        post_data = request.get_json()
        email = post_data.get('email')
        invite_code = post_data.get('invite_code')
        role = post_data.get()