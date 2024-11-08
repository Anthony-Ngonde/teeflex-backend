from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Define naming convention for database schema
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class User(db.Model,SerializerMixin):
    #Table to store the users information
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

class GymEquipment(db.Model,SerializerMixin):
    
    
    #Table to store the gym equipments
    __tablename__ = 'gym_equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<GymEquipment {self.name}>'
    

class PaymentDetails(db.Model):
    
    
    #Table to store the payment details
    __tablename__ = 'payment_details'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    plan = db.Column(db.String(20), nullable=False)  
    price = db.Column(db.Integer, nullable=False)
    paid_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False) 

    def __repr__(self):
        return f'<PaymentDetails {self.name} - {self.plan}>'

