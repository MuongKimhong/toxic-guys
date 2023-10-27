from django.urls import path

from notifications.views import *


urlpatterns = [
    path("get-all-notifications/", GetAllNotifications.as_view()),
    path("mark-notification-as-seen-by-receiver/", MarkNotificationsAsSeenByReceiver.as_view())
]