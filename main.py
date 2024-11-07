from flask import Flask
from flask_restful import Api, Resource
from config import DevConfig
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import os
from database import db, migrate  
from resources.gymequipment import GymEquipmentResource  
from resources.paymentdetails import PaymentDetailsResource
from resources.auth import SignUpResource, LoginResource
from resources.hello import HelloResource


app = Flask(__name__)
app.config.from_object(DevConfig)

CORS(app)


db.init_app(app)
migrate.init_app(app, db)

jwt = JWTManager(app)




api = Api(app)



# Endpoints
api.add_resource(HelloResource, '/hello')
api.add_resource(GymEquipmentResource, '/equipment', '/equipment/<int:equipment_id>')
api.add_resource(PaymentDetailsResource, '/payments', '/payments/<int:payment_id>')
api.add_resource(SignUpResource, '/signup', '/signup/<int:id>')
api.add_resource(LoginResource, '/login')



if __name__ == '__main__':
    app.run(debug=True)