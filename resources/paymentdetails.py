# Endpoint for performing CRUD operations on payments
from flask_restful import Resource, reqparse
from sqlalchemy import and_, not_
from models import db, Payment, Member, Active
from datetime import datetime, timedelta


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
            return {'message': 'Payment id is already used'}, 400

        # Making sure the user with the given number even exists

        member = Member.query.filter_by(
            phone_number=data['phone_number']).first()

        if not member:
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
            member_id=member.id
        )

        db.session.add(new_payment)

        # Calculate the expiry date based on the plabe

        plan_duration = {
            "monthly": 30,
            "weekly": 7,
            "daily": 1
        }

        duration = plan_duration.get(data['plan'].lower())

        if not duration:
            return {'message': "Invalid plan. Options are monthly,weekly,daily"}, 400

        expiry_date = payment_date + timedelta(duration)

        # Update or create the member's active subscription
        active_subscription = Active.query.filter_by(user_id=member.id).first()
        if active_subscription:
            # Extend the expiry date for an existing subscription
            if active_subscription.expiry_date < expiry_date:
                active_subscription.expiry_date = expiry_date
                active_subscription.status = True  # Reactivate the user's subscription plan

        else:
            # Create an new active subscription
            new_active = Active(
                status=True,
                date_paid=payment_date,
                expiry_date=expiry_date,
                user_id=member.id
            )
            db.session.add(new_active)

        # Commit the transaction
        db.session.commit()

        return {'message': 'Payment added', 'status': 'success'}, 201

    def get(self, id=None):

        # Endpoint for getting payments:

        # Fetching all payments that have been made
        if id == None:
            all_payments = Payment.query.all()

            return [payments.to_dict() for payments in all_payments]

        # Fetchin a single payment
        if id:
            payment = Payment.query.filter_by(id=id).first()

            if payment == None:
                return {'message': 'Payment not found'}
            return payment.to_dict()

    def patch(self, id):
        # Endpoint to update the payments

        data = self.parser.parse_args()

        payment = Payment.query.filter_by(id=id).first()

        if not payment:
            return {'message': "No payment to update"}
        else:
            payment_date = datetime.strptime(
                data['date'], '%Y-%m-%d')

        # Checking to confirm the number we are trying to update is there in our database
        phone_number = Member.query.filter_by(
            phone_number=data['phone_number']).first()

        if phone_number == None:
            return {'message': "Phone number not found"}

        # Checking if the transaction id already is there and belongs to a certain member
        transaction_id = db.session.query(Payment).filter(
            and_(Payment.transaction_id == data['transaction_id'],
                 not_(Payment.id == id))
        ).first()

        if transaction_id:
            return {"message": 'Transaction id is already in use'}

        payment.phone_number = data['phone_number']
        payment.transaction_id = data['transaction_id']
        payment.plan = data['plan']
        payment.amount = data['amount']
        payment.date = payment_date

        db.session.commit()

        return {'message': "Payment details updated successfully"}

    def delete(self, id):
        # We check if the payment even exists
        payment = Payment.query.filter_by(id=id).first()

        if payment == None:
            return {'message': "No payment to be deleted"}

        db.session.delete(payment)
        db.session.commit()

        return {'message': "Payment deleted successfuly"}
