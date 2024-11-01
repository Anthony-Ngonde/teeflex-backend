from flask import Flask
from flask_restful import Api, Resource
from config import DevConfig
import os
from database import db, migrate  
from resources.gymequipment import GymEquipmentResource  
from resources.paymentdetails import PaymentDetailsResource


app = Flask(__name__)
app.config.from_object(DevConfig)


db.init_app(app)
migrate.init_app(app, db)




api = Api(app)



# Endpoints

api.add_resource(GymEquipmentResource, '/equipment', '/equipment/<int:equipment_id>')
api.add_resource(PaymentDetailsResource, '/payments', '/payments/<int:payment_id>') 



if __name__ == '__main__':
    app.run()