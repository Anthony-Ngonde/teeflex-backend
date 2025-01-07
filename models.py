# Modelling the the database schema
import re
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime


# To ensure consistency in the naming of the constraints, we can define a naming convention that will be used by SQLAlchemy.
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# We then pass the naming convention to the MetaData object
metadata = MetaData(naming_convention=convention)

# We then create an instance of the SQLAlchemy class and pass the metadata object to it
db = SQLAlchemy(metadata=metadata)


class ValidationError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Member(db.Model, SerializerMixin):

    # Defining the table
    __tablename__ = 'members'

    # Defining the columns in our database
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    # Defining the relationship
    payment = db.relationship('Payment', back_populates='member')
    active = db.relationship('Active', back_populates='user')
    

    # Ensuring the email being saved is a valid email
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Please enter a valid email address.')
        return email

    # Ensuring the phone number is always valid before saving it in the database
    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if not re.match(r"^0[0-9]{9}$", phone_number):
            raise ValidationError(
                'Phone number must be a 10-digit number starting with 0')
        return phone_number


class Payment(db.Model, SerializerMixin):

    # Defining the table
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String, nullable=False)
    transaction_id = db.Column(db.String(10), nullable=False, unique=True)
    plan = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)

    # Serialize rules
    serialize_only = ('phone_number', 'transaction_id',
                      'plan', 'amount', 'date')

    member = db.relationship('Member', back_populates='payment')
    


# Table to keep track of the active members
class Active(db.Model, SerializerMixin):

    __tablename__ = 'actives'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    date_paid = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)

    user = db.relationship('Member', back_populates='active')
