# Designing the GUI for the application
# Importing the necessary libraries
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


from resources.notifications import NotificationResource, MarkNotificationReadResource
from resources.active import ActiveResource
from resources.paymentdetails import PaymentResource
from resources.members import MembersResource
from resources.admin import RegisterResource, LoginResource, LogoutResource
from resources.hello import HelloResource
from resources.greetings import GreetingResource
from models import db, RevokedToken


# Importing the db object

# Importing our endpoint

# Setting the expiry of our jwt_tokens
ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

# Initializing the API
api = Api(app)

# Configuring the app
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teeflex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = 'teeflex'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
# This is to solve the errror message of subject must a string in flask_jwt_extended
app.config['JWT_VERIFY_SUB'] = False

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


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(RevokedToken.id).filter_by(jti=jti).scalar()

    return token is not None


@staticmethod
def broadcast_notification(message):
    '''
    Broadcast a notification message to all connected clients via SocketIO
    '''
    socketio.emit('receive_notification', {'message': message}, broadcast=True)


# Creating an API object
api.add_resource(HelloResource, '/')
api.add_resource(GreetingResource, '/admin/name')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(MembersResource, '/members', '/members/<int:id>')
api.add_resource(PaymentResource, '/payments', '/payments/<int:id>')
api.add_resource(ActiveResource, '/actives', '/actives/<int:id>')
api.add_resource(NotificationResource, '/notifications',
                 '/notification/<int:id>')
api.add_resource(MarkNotificationReadResource, '/notification/<int:id>')
