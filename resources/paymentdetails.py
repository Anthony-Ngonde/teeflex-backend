from flask import request
from flask_restful import Resource
from database import db 
from models import PaymentDetails
from datetime import datetime, timedelta



class PaymentDetailsResource(Resource):
    def get(self, payment_id=None):
        """Retrieve all payment details or a specific  payment by ID."""
        if payment_id is None:
            payments = PaymentDetails.query.all()
            result = []
            for payment in payments:
                if payment.expiry_date < datetime.utcnow():
                    payment.status = 'Expired'
                    db.session.commit()  # Save the updated status in the database
                result.append({
                    'id': payment.id,
                    'name': payment.name,
                    'plan': payment.plan,
                    'price': payment.price,  # Include price here
                    'paid_date': payment.paid_date.isoformat(),
                    'expiry_date': payment.expiry_date.isoformat(),
                    'status': payment.status
                })
            return result, 200
        else:
            payment = PaymentDetails.query.get(payment_id)
            if payment:
                if payment.expiry_date < datetime.utcnow():
                    payment.status = 'Expired'
                    db.session.commit()
                return {
                    'id': payment.id,
                    'name': payment.name,
                    'plan': payment.plan,
                    'price': payment.price,  # Include price here
                    'paid_date': payment.paid_date.isoformat(),
                    'expiry_date': payment.expiry_date.isoformat(),
                    'status': payment.status
                }, 200
            return {'message': 'Payment details not found'}, 404

    
    def post(self):
        data = request.get_json()
        plan_duration = {'Daily': 1, 'Weekly': 7, 'Monthly': 30}
        paid_date = datetime.utcnow()
        expiry_date = paid_date + timedelta(days=plan_duration.get(data['plan'], 1))
        
        new_payment = PaymentDetails(
            name=data['name'],
            plan=data['plan'],
            price=data['price'],
            paid_date=paid_date,
            expiry_date=expiry_date,
            status='Active'
        )
        db.session.add(new_payment)
        db.session.commit()
        
        return {
            'message': 'Payment detail created',
            'id': new_payment.id,
            'name': new_payment.name,
            'plan': new_payment.plan,
            'price': new_payment.price,
            'paid_date': new_payment.paid_date.isoformat(),
            'expiry_date': new_payment.expiry_date.isoformat(),
            'status': new_payment.status
        }, 201
    

    def put(self, payment_id):
        """Update an existing payment detail entry."""
        payment = PaymentDetails.query.get(payment_id)
        if not payment:
            return {'message': 'Payment details not found'}, 404

        data = request.get_json()
        payment.name = data.get('name', payment.name)
        payment.plan = data.get('plan', payment.plan)
        payment.price = data.get('price', payment.price)  # Update price if provided

        # Update dates and status based on new plan
        plan_duration = {'Daily': 1, 'Weekly': 7, 'Monthly': 30}
        payment.paid_date = datetime.utcnow()
        payment.expiry_date = payment.paid_date + timedelta(days=plan_duration.get(payment.plan, 1))
        payment.status = 'Active' if payment.expiry_date > datetime.utcnow() else 'Expired'

        db.session.commit()
        return {'message': 'Payment details updated'}, 200

    def delete(self, payment_id):
        """Delete a payment detail entry."""
        payment = PaymentDetails.query.get(payment_id)
        if not payment:
            return {'message': 'Payment details not found'}, 404

        db.session.delete(payment)
        db.session.commit()
        return {'message': 'Payment detail deleted'}, 200
