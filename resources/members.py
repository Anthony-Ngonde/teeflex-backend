# The endpoint to perform all the CRUD operations
from flask_restful import Resource, reqparse
from models import db, Member


# TODO --> Check if the number is valid and also the email if it is valid
class MembersResource(Resource):

    # Create a nre instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument(
        'f_name', help='First name is required', required=True, type=str)
    parser.add_argument(
        'l_name', help='Last name is required', required=True, type=str)
    parser.add_argument(
        'phone_number', help='Phone number is required', required=True, type=str)
    parser.add_argument(
        'email', help='Email address is required', required=True, type=str)

    def post(self):

        # Endpoint responsible for adding new user instances to the database
        data = MembersResource.parser.parse_args()

        phone_number = Member.query.filter_by(
            phone_number=data['phone_number']).first()

        # Checking if the phone number is already in our database
        if phone_number:
            return {'message': "Phone number already exists"}, 422

        # Checking if the email instance already exists in our database
        email = Member.query.filter_by(email=data['email']).first()

        if email:
            return {'message': "Email already in use"}, 422

        new_member = Member(**data)

        # add the new member instance
        db.session.add(new_member)

        # Persisting the changes to the database
        db.session.commit()

        return {'message': 'New member added successfully'}

    def get(self, id=None):
        # The endpoint to perform the get requests

        # If an id is not passed we query all the members
        if id == None:
            all_members = Member.query.all()

            all_data = []

            for members in all_members:
                all_data.append(members.to_dict())

            return {'members': all_data}

        else:
          # If an id is passed we get the member with the given id
            one_member = Member.query.filter_by(id=id).first()

          # Checking if of the given id even exists
            if one_member == None:
                return {'message': 'Member not found'}, 404

            return one_member.to_dict()
