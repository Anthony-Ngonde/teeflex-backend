# Section to seed our database with data
from datetime import datetime
from app import app
from models import db, Payment, Member


with app.app_context():

    print('Starting to seed the database')
    Payment.query.delete()
    Member.query.delete()

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
                          date=datetime.strptime('2024-05-01','%Y-%m-%d'), member_id=member.id)
    db.session.add(new_payment)
    db.session.commit()

    print('Added new payment')
