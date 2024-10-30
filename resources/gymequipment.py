from flask import request
from flask_restful import Resource
from database import db 
from models import GymEquipment

class GymEquipmentResource(Resource):
    def get(self, equipment_id=None):
        """Retrieve all gym equipment or a specific item by ID."""
        if equipment_id is None:
            # Retrieve all equipment
            equipment = GymEquipment.query.all()
            return [{'id': eq.id, 'name': eq.name, 'equipment_type': eq.equipment_type, 
                     'quantity': eq.quantity, 'description': eq.description} for eq in equipment], 200
        else:
            # Retrieve specific equipment by ID
            equipment = GymEquipment.query.get(equipment_id)
            if equipment:
                return {'id': equipment.id, 'name': equipment.name, 'equipment_type': equipment.equipment_type,
                        'quantity': equipment.quantity, 'description': equipment.description}, 200
            return {'message': 'Equipment not found'}, 404

    def post(self):
        """Create a new gym equipment entry."""
        data = request.get_json()
        new_equipment = GymEquipment(
            name=data['name'],
            equipment_type=data['equipment_type'],
            quantity=data['quantity'],
            description=data.get('description', '')
        )
        db.session.add(new_equipment)
        db.session.commit()
        return {'message': 'Equipment created', 'id': new_equipment.id}, 201

    def put(self, equipment_id):
        """Update an existing gym equipment entry."""
        equipment = GymEquipment.query.get(equipment_id)
        if not equipment:
            return {'message': 'Equipment not found'}, 404

        data = request.get_json()
        equipment.name = data.get('name', equipment.name)
        equipment.equipment_type = data.get('equipment_type', equipment.equipment_type)
        equipment.quantity = data.get('quantity', equipment.quantity)
        equipment.description = data.get('description', equipment.description)

        db.session.commit()
        return {'message': 'Equipment updated'}, 200

    def delete(self, equipment_id):
        """Delete a gym equipment entry."""
        equipment = GymEquipment.query.get(equipment_id)
        if not equipment:
            return {'message': 'Equipment not found'}, 404
        
        db.session.delete(equipment)
        db.session.commit()
        return {'message': 'Equipment deleted'}, 200