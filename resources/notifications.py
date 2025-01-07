#Endpoint for handling our notifications
from flask_restful import Resource
from models import Notification

class NotificationResource(Resource):

    #This will be just support get methods
    def get(self):
        notifications = Notification.query.order_by(Notification.created_at.desc()).all()
        
        return [notification.to_dict() for notification in notifications]