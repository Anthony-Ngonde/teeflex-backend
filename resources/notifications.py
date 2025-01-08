# Endpoint for handling our notifications
from flask_restful import Resource
from models import db, Notification


class NotificationResource(Resource):

    # This will be just support get methods
    def get(self):
        notifications = Notification.query.order_by(
            Notification.created_at.desc()).all()

        return [notification.to_dict() for notification in notifications]


class MarkNotificationReadResource(Resource):

    # This will be the endpoint to mark our notifications as read
    def patch(self, id):
        notification = Notification.query.get(id)
        if not notification:
            return {'message': "No recent updates"}, 404

        notification.is_read = True

        db.session.commit()

        return {'message': 'Notification marked as read'}