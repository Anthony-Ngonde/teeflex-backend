from exts import db
from datetime import datetime



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
