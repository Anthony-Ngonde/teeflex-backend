from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
import jwt
import datetime
from config import DevConfig
from flask_jwt_extended import create_access_token, create_refresh_token



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
        
        
        username = data.get('username')
        password = data.get('password')

    
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid credentials'}), 401

    
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200