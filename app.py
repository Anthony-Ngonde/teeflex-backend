import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db

# Factory function for creating the Flask app
def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    Migrate(app, db)
    Bcrypt(app)
    JWTManager(app)

    # Register resources
    register_resources(app)

    return app


# Configuration dictionary for different environments
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.environ.get('JWT_SECRET', 'default_secret_key')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///teeflex.db'


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


# Function to register all API resources
def register_resources(app):
    api = Api(app)
    from resources.hello import HelloResource
    from resources.members import MembersResource
    from resources.paymentdetails import PaymentResource

    api.add_resource(HelloResource, '/')
    api.add_resource(MembersResource, '/members', '/members/<int:id>')
    api.add_resource(PaymentResource, '/payments', '/payments/<int:id>')
