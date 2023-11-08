from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers
from django.db.models import Q
from itertools import chain

from users.utils import token_verification
from users.models import User
from chats.models import ChatRoom, Message
from chats.models import GroupChatRoom, GroupMessage
from groups.models import Group
import json


class GetChatRoomList(APIView):
    permission_classes = [ IsAuthenticated ]

    '''
    chatroom that has the latest last_message_created_date will be the first
    '''
    def sort_chatrooms(self, combined_chatrooms_q):
        sorted_chatrooms = sorted(combined_chatrooms_q, key=lambda instance: instance.last_message_created_date ) 
        sorted_chatrooms.reverse()
        sorted_chatrooms = [room.serialize() for room in sorted_chatrooms]
        return sorted_chatrooms

    def get(self, request):
        user_id = token_verification(request)
        chatrooms_q = ChatRoom.objects.filter(Q(creator__id=user_id) | Q(member__id=user_id))
        group_chatrooms_q = GroupChatRoom.objects.filter(members=user_id)

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
        chatroom.last_message_text = message.text
        chatroom.last_message_sender_name = message.sender.username
        chatroom.save()
        return Response({"message": message.serialize()}, status=200)


class SendMessageForGroupChatRoom(SendMessage):
    chatroom_model = GroupChatRoom
    chatroom_type  = "group"


class DeleteMessage(APIView):
    permission_classes = [ IsAuthenticated ]

    def action(self, message, request):
        message.delete()

    def post(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        message_type = request.data.get("message_type")

        if (message_type != "user") and (message_type != "group"):
            return Response({"wrong_param": True}, status=400)

        if message_type == "user":
            try:
                message = Message.objects.get(id=request.data["message_id"], sender__id=user.id)
            except Message.DoesNotExist:
                return Response({"message_err": True}, status=400)
        elif message_type == "group":
            try:
                message = GroupMessage.objects.get(id=request.data["message_id"], sender__id=user.id)
            except GroupMessage.DoesNotExist:
                return Response({"message_err": True}, status=400)

        self.action(message, request)
        return Response({"success": True}, status=200)


class UpdateMessage(DeleteMessage):
    def action(self, message, request):
        message.text = request.data.get("new_message_text")
        message.save()


class SendMessageAsImage(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ parsers.MultiPartParser ]

    def post(self, request):
        chatroom = ChatRoom.objects.get(id=request.data["room_id"])
        images = json.loads(request.data["images"])

        message = Message.objects.create(sender_id=token_verification(request), chatroom_id=chatroom.id)       

        for image in images:
            message_image = MessageImage.objects.create(image=image)
            message.images.add(message_image)

        return Response({"message": message.serialize()}, status=200)
