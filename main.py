from flask import Flask
from flask_restful import Api, Resource
from config import DevConfig
import os
from database import db, migrate  
from resources.gymequipment import GymEquipmentResource  


app = Flask(__name__)
app.config.from_object(DevConfig)


db.init_app(app)
migrate.init_app(app, db)




api = Api(app)

# class HelloResource(Resource):
#     def get(self):
#         """Return a greeting message."""
#         return {"message": "Hello, World!"}, 200


# api.add_resource(HelloResource, '/hello') 

api.add_resource(GymEquipmentResource, '/equipment', '/equipment/<int:equipment_id>')


if __name__ == '__main__':
    app.run()