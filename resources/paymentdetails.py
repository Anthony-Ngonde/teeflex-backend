# Endpoint for performing CRUD operations on payments
from flask_restful import Resource, reqparse
from models import db, Payment, Member
from datetime import datetime


class PaymentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'phone_number', help='Phone number is required', required=True, type=str)
    parser.add_argument(
        'transaction_id', help='Transaction id must be included', required=True, type=str)
    parser.add_argument(
        'plan', help='Plan taken by the member is required', required=True, type=str)
    parser.add_argument('amount', help='Add amount', required=True, type=int)
    parser.add_argument('date', help='Date is required',
                        required=True, type=str)

    def post(self):
        # Endpoint for adding new payment
        data = PaymentResource.parser.parse_args()

        # Checking if the transaction id is already available in our database to avoid duplication
        payment_id = Payment.query.filter_by(
            transaction_id=data['transaction_id']).first()
        # Checking if the payment id is already in our database
        if payment_id:
            return {'message': 'Payment id is already used'}

        # Making sure the user with the given number even exists

        phone_no = Member.query.filter_by(phone_number=data['phone_number']).first()

        if not phone_no:
            return {'message': 'Member does not exist'}

        # Parse the date into a datetime object
        try:
            payment_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return {'message': 'Invalid date format'}

        new_payment = Payment(
            phone_number=data['phone_number'],
            transaction_id=data['transaction_id'],
            plan=data['plan'],
            amount=data['amount'],
            date=payment_date,
            member_id=phone_no.id
        )

        db.session.add(new_payment)

        db.session.commit()

        return {'message': "Payment added"}
