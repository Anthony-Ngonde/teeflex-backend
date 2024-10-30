from datetime import datetime
from main import db

class GymEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<GymEquipment {self.name}>'

class PaymentDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    plan = db.Column(db.String(20), nullable=False)  
    paid_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False) 

    def __repr__(self):
        return f'<PaymentDetails {self.name} - {self.plan}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'