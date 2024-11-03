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
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        
        if User.query.filter_by(email=email).first():
            return {"message": "User with this email already exists"}, 400

        
        hashed_password = generate_password_hash(password)

        
        new_user = User(name=name, email=email, password=hashed_password)

        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

