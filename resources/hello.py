from flask import request
from flask_restful import Resource
from database import db 


class HelloResource(Resource):
    def get(self):
        return {"message": "Hello, World!"}, 200
