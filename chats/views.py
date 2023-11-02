from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers
from django.db.models import Q

from users.utils import token_verification
from chats.models import ChatRoom, Message, MessageImage
from groups.models import Group


class GetChatRoomList(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user_id = token_verification(request)
        chatrooms = ChatRoom.objects.filter(Q(creator__id=user_id) | Q(member__id=user_id))
        chatrooms = [chatroom.serialize() for chatroom in chatrooms]
        return Response({"chatrooms": chatrooms}, status=200) 
