#Designing the GUI for the application
#Importing the necessary libraries
from flask import Flask
from flask_restful import Api

#Importing our endpoint
from resources.hello import HelloResource

app = Flask(__name__)

api = Api(app)

#Creating an API object
api.add_resource(HelloResource, '/')


