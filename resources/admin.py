# The admin section part for accessing the application
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models import db, Admin, ValidationError


class RegisterResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'first_name', help='Enter your first name', required=True, type=str)
    parser.add_argument(
        'last_name', help='Enter your last name', required=True, type=str)
    parser.add_argument('email', help='Enter a valid email',
                        required=True, type=str)
    parser.add_argument(
        'password', help='Enter your password', required=True, type=str)

    def post(self):

        # Logic to handle new user registration
        data = self.parser.parse_args()

        # Checking if the email is already in use
        email = Admin.query.filter_by(email=data['email']).first()

        if email:
            return {'message': "Email already exists", 'status': 'fail'}, 422

        try:
            admin = Admin(**data)
            
            db.session.add(admin)

            db.session.commit()

            return {'message': 'Registration successful', 'status': 'success'}
        except ValidationError as e:
            return {'message': str(e), 'status': 'fail'}, 422


class LoginResource(Resource):

    '''Class to handle login logic'''

    parser = reqparse.RequestParser()
    parser.add_argument('email', help='Email is reuired',
                        required=True, type=str)
    parser.add_argument(
        'password', help='Input valid password', required=True, type=str)

    def post(self):

        data = self.parser.parse_args()

        if_admin = Admin.query.filter_by(email=data['email']).first()

        if if_admin:

            # Checking to confirm if the credentials match
            is_password_match = if_admin.check_password(data['password'])

            if is_password_match:
                user_dict = if_admin.to_dict()

                # If credentials are valid we give them an access token

                access_token = create_access_token(identity=user_dict['id'])

                return {
                    'message': 'Login successful',
                    "status": 'success',
                    "admin": user_dict,
                    "jwt_token": access_token
                }, 201

            else:
                return {'message': 'Invalid email/password', 'status': 'fail'}, 403
        else:
            return {'message': 'Invalid email/password', 'status': 'fail'}, 403
