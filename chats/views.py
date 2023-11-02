from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers
from django.db.models import Q

from users.utils import token_verification
from users.models import User
from chats.models import ChatRoom, Message, MessageImage
from groups.models import Group


class GetChatRoomList(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user_id = token_verification(request)
        chatrooms = ChatRoom.objects.filter(Q(creator__id=user_id) | Q(member__id=user_id))
        chatrooms = [chatroom.serialize() for chatroom in chatrooms]
        return Response({"chatrooms": chatrooms}, status=200) 


class GetMessagesInChatRoom(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        try:
            chatroom = ChatRoom.objects.get(id=request.query_params["chatroom_id"])
        except ChatRoom.DoesNotExist:
            return Response({"no_chatroom": True}, status=400)
        
        messages = Message.objects.filter(chatroom__id=chatroom.id).order_by("-id")
        messages = [message.serialize() for message in messages]

        return Response({"messages": messages}, status=200)


class SendMessage(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            sender = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"sender_err": True}, status=400)
        
        try:
            chatroom = ChatRoom.objects.get(id=request.data["chatroom_id"])
        except ChatRoom.DoesNotExist:
            return Response({"chatroom_err": True}, status=400)

        message = Message.objects.create(
            chatroom=chatroom,
            sender=sender,
            receiver_id=request.data["receiver_id"],
            text=request.data["text"]
        )
        return Response({"message": message.serialize()}, status=200)
