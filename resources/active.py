# Endpoint to check on whether the user has an active subscription or not
from flask_restful import Resource, reqparse
from models import db, Active, Payment, Member
from datetime import datetime


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

    def get(self, id=None):

        current_date = datetime.now()

        #Getting all members in the database
        members = Member.query.filter_by(id=id).first()
        print(members)
        
        # Query all active members and update their status if expired
        all_active_members = Active.query.all()
        
        for member in all_active_members:

            '''
            I ran into a problem 'TypeError: must be string, not datetime.datetime when using strptime'
            The solution i got was to first convert the date and time to a string before passing it into the strptime
            '''
            # print(f'Line 27:{type(member.expiry_date)}')
            convt_date = str(member.expiry_date)
            expiry_date = datetime.strptime(convt_date, '%Y-%m-%d %H:%M:%S')

            if current_date >= expiry_date and member.status:
                member.status = False
                db.session.commit()

        # Fetch and return all members or a specific member
        if id is None:
            # print(member.to_dict())
            all_active = [member.to_dict() for member in all_active_members]
            
            return {'active':all_active}

        active_member = Active.query.filter_by(id=id).first()
        
        if active_member is None:
            return {'message': 'No such member', 'status': 'fail'}, 404
        
        return active_member.to_dict()

    # TODO --> Send SMS to users whose subscription is almost over
