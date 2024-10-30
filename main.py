from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevConfig
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(DevConfig)

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Restful API
api = Api(app)

# Import models after db initialization
import models

# Test Resource
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World"}

api.add_resource(HelloResource, '/hello')

# Run the app
if __name__ == '__main__':
    app.run()