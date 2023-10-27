from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView

from notifications.models import Notification
from users.models import User
from users.utils import token_verification


def send_notification(sender, receiver, text, _type=None):

    notification = Notification.objects.get_or_create(
        sender = sender,
        receiver = receiver,
        text = text
    )
    if _type is not None:
        notification._type = _type
        notification.save()


class GetAllNotifications(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"token_error": True}, status=400)
        
        notifications = Notification.objects.filter(receiver__id=user.id).order_by("-id")
        notifications = [notification.serialize() for notification in notifications]

        return Response({"notifications": notifications}, status=200)


class MarkNotificationsAsSeenByReceiver(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        notifications = Notification.objects.filter(receiver__id=token_verification(request))
        
        for notification in notifications:
            if notification.seen_by_receiver is False:
                notification.seen_by_receiver = True
                notification.save()
        
        return Response({"seen_all": True}, status=200)
