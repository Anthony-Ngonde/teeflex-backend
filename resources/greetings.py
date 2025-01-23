#Api for sending back the greeting to the admin
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import Admin

class GreetingResource(Resource):

    @jwt_required()
    def get(self):
        #To get the name admin
        user_id = get_jwt_identity()
        user = Admin.query.filter_by(id=user_id).first()
       
        if user:
            admin_name = Admin.query.get(user.id)
            
            return admin_name.to_dict()
            
            
            

        