# Modelling the the database schema
import re
from sqlalchemy import MetaData
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

# TODO --> Check relationship of member and payment

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


class Admin(db.Model, SerializerMixin):

    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(225), nullable=False)

    # Serializer rules
    serialize_rules = ('-password',)
    # Ensuring the email is in the correct format before adding it to our database

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Please enter a valid email address.')
        return email

    # Checking the strength of the password
    @validates('password')
    def password_strength(self, key, password):

        # Regular expressions for uppercase,lowercase and numeric characters
        if len(password) < 8:
            raise ValidationError(
                'Password is too short, it should be have minimum of 8 characters'
            )
        if not re.search('[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter'
            )
        if not re.search('[a-z]', password):
            raise ValidationError(
                'Password must contain at least on lowercase letter'
            )
        if not re.search('[0-9]', password):
            raise ValidationError(
                'Password must contain at least on number'
            )

         # Hashing the password before doing the validation
        return generate_password_hash(password).decode('utf-8')

    # Hashing the password before saving it to our database

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)


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
    payment = db.relationship('Payment', back_populates='member',cascade="all, delete-orphan")

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
    date = db.Column(db.DateTime, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)

    # Serialize rules
    serialize_only = ('phone_number', 'transaction_id',
                      'plan', 'amount', 'date', 'member_id')

    member = db.relationship('Member', back_populates='payment')
    active = db.relationship('Active', back_populates='user',cascade="all, delete-orphan")


class Active(db.Model, SerializerMixin):
    __tablename__ = 'actives'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=False)
    date_paid = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    name = db.Column(db.String, nullable=False)  
    # Serializer rules
    serialize_only = ('status', 'date_paid', 'expiry_date', 'user_id', 'name')

    user = db.relationship('Payment', back_populates='active')


class Notification(db.Model, SerializerMixin):

    # Class/Table to keep track of any notifications
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Short description
    message = db.Column(db.Text, nullable=False)  # Detailed info
    # e.g payment, 'member'
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_read = db.Column(db.Boolean, default=False)  # Track read/unread state
