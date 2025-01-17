# Designing the GUI for the application
# Importing the necessary libraries
import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Importing the db object
from models import db

# Importing our endpoint
from resources.hello import HelloResource
from resources.admin import RegisterResource, LoginResource
from resources.members import MembersResource
from resources.paymentdetails import PaymentResource
from resources.active import ActiveResource
from resources.notifications import NotificationResource, MarkNotificationReadResource

app = Flask(__name__)

# Initializing the API
api = Api(app)

# Configuring the app
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teeflex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')


# Binding the app to the db object
db.init_app(app)

# Enabling CORS
CORS(app)

# Initializing socketIO
socketio = SocketIO(app)

# Migrating the database
migrate = Migrate(app, db)

# Initiliazing the bcrypt object
bcrypt = Bcrypt(app)

# Initializing the JWTManager object
jwt = JWTManager(app)


@staticmethod
def broadcast_notification(message):
    '''
    Broadcast a notification message to all connected clients via SocketIO
    '''
    socketio.emit('receive_notification', {'message': message}, broadcast=True)


# Creating an API object
api.add_resource(HelloResource, '/')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(MembersResource, '/members', '/members/<int:id>')
api.add_resource(PaymentResource, '/payments', '/payments/<int:id>')
api.add_resource(ActiveResource, '/actives', '/actives/<int:id>')
api.add_resource(NotificationResource, '/notifications')
api.add_resource(MarkNotificationReadResource, '/notification/<int:id>')
