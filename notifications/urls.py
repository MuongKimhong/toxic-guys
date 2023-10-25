from django.urls import path

from notifications.views import *

urlpatterns = [
    path("get-all-notifications/", GetAllNotifications.as_view())
]