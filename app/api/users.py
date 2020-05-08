from flask import Blueprint,request,jsonify
from flask_restx import Resource,Api,fields
from app import db
from app.api.models import User,Invited_user

users_blueprint = Blueprint('users',__name__)
api = Api(users_blueprint)

user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    # 'role':fields.Integer(required=True),
    'email': fields.String(required=True),
    'name': fields.String(required=True),
    'password': fields.String(required=True)
})
user_login = api.model('User',{
    'id': fields.Integer(readOnly=True),
    # 'role':fields.Integer(required=False),
    'email': fields.String(required=True),
    'name': fields.String(required=False),
    'password': fields.String(required=True)
})

class SignUp(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        name = post_data.get('name')
        email = post_data.get('email')
        password = post_data.get('password')
        invite_code = post_data.get('invite_code')
        response_object={}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry, That email already exists.'
            return response_object,400

        invited_user = Invited_user.query.filter_by(email=email,invite_code=invite_code).first()
        if invited_user:
            db.session.add(User(name=name,email=email,password=password,role_id=invited_user.role_id))
            db.session.commit()
            response_object['message'] = f'{email} was added!'
            print(response_object)
            return response_object,201
        else:
            response_object['message'] = 'Not authorised'
            return response_object,401
api.add_resource(SignUp,'/users')

class AllUsers(Resource):
    @api.marshal_with(user)
    def get(self):
        users = User.query.all()
        return users
api.add_resource(AllUsers,'/allusers')

class Users(Resource):
    @api.marshal_with(user)
    def get(self,user_id):
        user = User.query.filter_by(id=user_id).first()
        rsp={}
        if not user:
            api.abort(404, f'User {user_id} does not exist')
        return user.json(),200
api.add_resource(Users,'/users/<int:user_id>')

class LogIn(Resource):
    @api.expect(user_login, validate=True)
    def post(self):
        post_data = request.get_json()
        email =post_data.get('email')
        password = post_data.get('password')
        user =User.query.filter_by(email=email).first()
        response_object={}
        
        if user.password != password:

            return 'Wrong password',401
        if  not user:
            response_object['message'] = f'{email} does not exist'
            return response_object,404
        return user.json(),200

api.add_resource(LogIn,'/login')