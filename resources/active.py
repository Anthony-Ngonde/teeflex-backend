# Endpoint to check on whether the user has an active subscription or not
from flask_restful import Resource, reqparse
from models import db, Active


class ActiveResource(Resource):

    parser = reqparse.RequestParse()
    parser.add_arguments(
        'status', help='Status of users payment', required=True, type=bool)
    parser.add_argumnents(
        'date_paid', help='Date paid is required', required=True, type=str)
    parser.add_argumnents(
        'expiry_date', help='Expiry date', required=True, type=str)
    parser.add_argumnents(
        'user_id', help='User id is required', required=True, type=int)
