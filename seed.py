# Section to seed our database with data
from datetime import datetime
from app import app
from models import db, Payment, Member, Active


with app.app_context():

    print('Starting to seed the database')
    Payment.query.delete()
    Member.query.delete()
    Active.query.delete()

    print('Seeding new members')
    member = Member(f_name='John', l_name='Doe',
                    phone_number='0758431218', email='john@gmail.com')

    db.session.add(member)
    db.session.commit()

    print('New member added')

    print('Seeding new payment')

    new_payment = Payment(phone_number='0758431218',
                          transaction_id='075934122', plan='monthly',
                          amount=500,
                          date=datetime.strptime('2024-05-01', '%Y-%m-%d'), member_id=member.id)
    db.session.add(new_payment)
    db.session.commit()

    print('Added new payment')

    print('Seeding member\'s activity')
    subscription = Active(status=True, date_paid=datetime.strptime(
        '2024-05-01', '%Y-%m-%d'), expiry_date=datetime.strptime('2024-05-02', '%Y-%m-%d'), user_id=member.id)
    db.session.add(subscription)
    db.session.commit()
    print('Finished adding member\'s activity')
