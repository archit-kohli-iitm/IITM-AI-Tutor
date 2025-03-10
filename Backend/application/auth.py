from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import mydb, User

auth_ns = Namespace('Auth', description="Authentication operations")

# -----------------------------------
#             SIGNUP
# -----------------------------------
base_auth = auth_ns.model('BaseAuth', {
    'email': fields.String(required=True, description="User email (must be unique)"),
    'password': fields.String(required=True, description="User password"),
})

signup_model = auth_ns.inherit('Signup', base_auth, {
    'name': fields.String(required=True, description="Full name"),
    'phone': fields.String(required=False, description="Phone number"),
    'dob': fields.String(required=False, description="Date of birth"),
    'utype': fields.String(required=False, default="tpstudent", description="User type (Default: tpstudent)"),
})

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.doc(
        responses={
            201: 'Successful registeration',
            400: 'User already exists',
            500: 'Internal Server Error'
        },
        description="Create and authenticate a new user into the application (Returns a JWT `access_token` to be included with every request)"
    )
    def post(self):
        """Create and authenticate a new user into the application"""
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'User already exists'}, 400
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            phone=data.get('phone', '0000000000'),
            dob=data.get('dob', '1900-01-01'),
            utype=data.get('utype', "tpstudent")
        )
        
        mydb.session.add(new_user)
        mydb.session.commit()
        
        access_token = create_access_token(identity=new_user.email)

        return {
            'message': 'User registered successfully',
            'access_token': access_token
        }, 201


# -----------------------------------
#               LOGIN
# -----------------------------------
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(base_auth)
    @auth_ns.doc(
        responses={
            200: 'Successful login',
            401: 'Invalid email or password',
            500: 'Internal Server Error'
        },
        description="Authenticate an existing user into the application (Returns a JWT `access_token` to be included with every request)"
    )
    def post(self):
        """Authenticate and login to the application"""
        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.email)

        return {'message': 'Login successful', 'access_token': access_token}, 200


# -----------------------------------
#               LOGOUT
# -----------------------------------
@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    @auth_ns.doc(
        responses={
            200: 'Successful logout',
            422: 'Invalid Token'
        }
    )
    def post(self):
        """Log out of the application"""
        return {'message': 'Logout successful'}, 200