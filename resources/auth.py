from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
import jwt
import datetime
from config import DevConfig
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token



class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        
        if User.query.filter_by(email=email).first():
            return {"message": "Member with this email already exists"}, 400

        
        hashed_password = generate_password_hash(password)

        
        new_user = User(name=name, email=email, password=hashed_password)

        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Member registered successfully"}, 201
    
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if user:
                return {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }, 200
            return {"message": "Member not found"}, 404
        else:
            users = User.query.all()
            users_data = [
                {"id": user.id, "name": user.name, "email": user.email}
                for user in users
            ]
            return {"users": users_data}, 200

    def put(self, id):
        data = request.get_json()
        user = User.query.get(id)

        if not user:
            return {"message": "Member not found"}, 404

        # Update user details
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        
        if 'password' in data:
            user.password = generate_password_hash(data['password'])

        db.session.commit()
        return {"message": "Member updated successfully"}, 200

    def delete(self, id):
        user = User.query.get(id)

        if not user:
            return {"message": "Member not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "Member deleted successfully"}, 200

    

class LoginResource(Resource):
     def post(self):
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')

        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401


        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200


