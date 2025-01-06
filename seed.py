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
