from django.urls import path
from chats.views import *


urlpatterns = [
    path("get-chatroom-list/", GetChatRoomList.as_view()),
    path("send-message/", SendMessage.as_view()),
    path("send-message-for-group-chatroom/", SendMessageForGroupChatRoom.as_view()),
    path("get-messages-in-chatroom/", GetMessagesInChatRoom.as_view()),
    path("get-messages-in-group-chatroom/", GetMessageInGroupChatRoom.as_view()),
    path("delete-message/", DeleteMessage.as_view()),
    path("update-message/", UpdateMessage.as_view()),
]