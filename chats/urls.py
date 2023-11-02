from django.urls import path
from chats.views import *


urlpatterns = [
    path("get-chatroom-list/", GetChatRoomList.as_view())
]