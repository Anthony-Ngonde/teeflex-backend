# Endpoint to check on whether the user has an active subscription or not
from flask_restful import Resource, reqparse
from models import db, Active


class ActiveResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'status', help='Status of users payment', required=True, type=bool)
    parser.add_argument(
        'date_paid', help='Date paid is required', required=True, type=str)
    parser.add_argument(
        'expiry_date', help='Expiry date', required=True, type=str)
    parser.add_argument(
        'user_id', help='User id is required', required=True, type=int)
    
    
    def get(self,id=None):
        
        #The endpoint to fetch the active members
        
        if id == None:
            active_members = Active.query.all()
            
            return [active.to_dict() for active in active_members]
