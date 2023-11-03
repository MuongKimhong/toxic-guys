from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers
from django.db.models import Q
from itertools import chain

from users.utils import token_verification
from users.models import User
from chats.models import ChatRoom, Message, MessageImage
from chats.models import GroupChatRoom, GroupMessage, GroupMessageImage
from groups.models import Group


class GetChatRoomList(APIView):
    permission_classes = [ IsAuthenticated ]

    def sort_chatrooms(self, combined_chatrooms_q):
        sorted_chatrooms = sorted(
            combined_chatrooms_q, key=lambda instance: instance.last_message_created_date
        )
        sorted_chatrooms.reverse()
        sorted_chatrooms = [room.serialize() for room in sorted_chatrooms]
        return sorted_chatrooms

    def get(self, request):
        user_id = token_verification(request)
        chatrooms_q = ChatRoom.objects.filter(Q(creator__id=user_id) | Q(member__id=user_id))
        chatrooms = [chatroom.serialize() for chatroom in chatrooms_q]

        group_chatrooms_q = GroupChatRoom.objects.filter(members=user_id).distinct()
        group_chatrooms = [chatroom.serialize() for chatroom in group_chatrooms_q]

        combined_chatrooms_q = chain(chatrooms_q, group_chatrooms_q)
        sorted_chatrooms = self.sort_chatrooms(combined_chatrooms_q)

        return Response({"chatrooms": sorted_chatrooms}, status=200) 


class GetMessagesInChatRoom(APIView):
    permission_classes = [ IsAuthenticated ]
    chatroom_model = ChatRoom
    chatroom_type = "user"
    param_keyword = "chatroom_id"

    def get(self, request):
        try:
            chatroom = self.chatroom_model.objects.get(id=request.query_params[f"{self.param_keyword}"])
        except self.chatroom_model.DoesNotExist:
            return Response({"no_chatroom": True}, status=400)
        
        if self.chatroom_type == "user":
            messages = Message.objects.filter(chatroom__id=chatroom.id)
        elif self.chatroom_type == "group":
            messages = GroupMessage.objects.filter(group_chatroom__id=chatroom.id)

        messages = [message.serialize() for message in messages]
        return Response({"messages": messages}, status=200)


class GetMessageInGroupChatRoom(GetMessagesInChatRoom):
    chatroom_model = GroupChatRoom
    chatroom_type  = "group"
    param_keyword  = "group_chatroom_id"


class SendMessage(APIView):
    permission_classes = [ IsAuthenticated ]
    chatroom_model = ChatRoom
    chatroom_type  = "user"

    def post(self, request):
        try:
            sender = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"sender_err": True}, status=400)
        
        try:
            chatroom = self.chatroom_model.objects.get(id=request.data["chatroom_id"])
        except self.chatroom_model.DoesNotExist:
            return Response({"chatroom_err": True}, status=400)

        if self.chatroom_type == "user":
            message = Message.objects.create(
                chatroom=chatroom,
                sender=sender,
                receiver_id=request.data["receiver_id"],
                text=request.data["text"]
            )
        elif self.chatroom_type == "group":
            message = GroupMessage.objects.create(
                group_chatroom=chatroom,
                sender=sender,
                text=request.data["text"]
            )
        chatroom.last_message_created_date = message.created_date
        chatroom.save()
        return Response({"message": message.serialize()}, status=200)


class SendMessageForGroupChatRoom(SendMessage):
    chatroom_model = GroupChatRoom
    chatroom_type  = "group"
