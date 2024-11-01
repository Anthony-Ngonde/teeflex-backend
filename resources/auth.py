from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
import jwt
import datetime
from config import DevConfig



class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'User already exists'}, 409

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid credentials'}, 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, DevConfig.SECRET_KEY, algorithm="HS256")

        return {'message': 'Login successful', 'token': token}, 200