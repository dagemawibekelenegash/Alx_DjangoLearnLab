# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by(
            "-timestamp"
        )

        unread_notifications = notifications.filter(is_read=False)

        notification_data = [
            {
                "actor": notification.actor.username,
                "verb": notification.verb,
                "timestamp": notification.timestamp,
                "is_read": notification.is_read,
            }
            for notification in unread_notifications
        ]

        return Response(notification_data, status=status.HTTP_200_OK)
