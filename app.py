import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


from models import db
from resources.gymequipment import GymEquipmentResource  
from resources.paymentdetails import PaymentDetailsResource
from resources.auth import SignUpResource, LoginResource
from resources.hello import HelloResource

#App initialization
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teeflex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get(
    'SECRET_KEY')


CORS(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
jwt = JWTManager(app)



# Endpoints
api.add_resource(HelloResource, '/hello')
api.add_resource(GymEquipmentResource, '/equipment', '/equipment/<int:equipment_id>')
api.add_resource(PaymentDetailsResource, '/payments', '/payments/<int:payment_id>')
api.add_resource(SignUpResource, '/signup', '/signup/<int:id>')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)









