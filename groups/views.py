from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework import parsers
from django.core.cache import cache

from notifications.models import Notification
from notifications.views import send_notification
from groups.models import Group, GroupInvitation, GroupMember
from chats.models import GroupChatRoom
from users.models import User
from users.utils import token_verification
from datetime import datetime
from random import sample
import json


TEN_MINUTES_IN_SECONDS = 10 * 60


class CreateGroup(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ parsers.MultiPartParser ]

    def post(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_not_found": True}, status=400)
        
        if request.data["group_name"].strip() == "" or request.data["group_type"].strip() == "":
            return Response({"data_missing": True}, status=400)
        
        group = Group.objects.create(
            creator=user,
            name=request.data["group_name"],
            description=request.data["group_description"],
        )
        if request.data["group_type"] == "Public":
            group.is_public = True
            group.is_private = False
        elif request.data["group_type"] == "Private":
            group.is_public = False
            group.is_private = True

        if isinstance(request.data["group_profile"], InMemoryUploadedFile):
            group.profile = request.data["group_profile"]
        
        group.save()

        # when group is created, create an empty group chatroom 
        group_chatroom = GroupChatRoom.objects.create(group=group, last_message_created_date=datetime.now())
        group_chatroom.members.add(user)
        return Response({"group_created": True}, status=200)


class InviteUserToJoinGroup(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ parsers.MultiPartParser ]

    def post(self, request):
        try:
            group = Group.objects.get(id=request.data["group"])
        except Group.DoesNotExist:
            return Response({"group_err": True}, status=400)

        invited_user_ids = json.loads(request.data["invited_user_ids"])

        notification_sender = User.objects.get(id=token_verification(request))

        for _id in invited_user_ids:
            try:
                user = User.objects.get(id=_id)
            except User.DoesNotExist:
                return Response({"user_err": True}, status=400)

            group_invitation, created = GroupInvitation.objects.get_or_create(
                group=group, user=user, inviter_id=token_verification(request)
            )
            send_notification(
                sender=notification_sender,
                receiver=user,
                text=f"{notification_sender.username} has invited you to join {group.name}",
                _type="group_invitation",
                group_inv=group_invitation
            )
        return Response({"invitation_sent": True}, status=200)


class AcceptGroupInvitation(APIView):
    permission_classes = [ IsAuthenticated ]
    status = "accept"

    def post(self, request):
        try:
            group_inv = GroupInvitation.objects.get(id=request.data["group_invitation_id"])
        except GroupInvitation.DoesNotExist:
            return Response({"group_inv_err": True}, status=400)

        if self.status == "accept": 
            group_member, created = GroupMember.objects.get_or_create(
                group=group_inv.group,
                user=group_inv.user
            )
            group_chatroom = GroupChatRoom.objects.get(group__id=group_inv.group.id)
            
            if group_inv.user not in group_chatroom.members.all(): 
                group_chatroom.members.add(group_inv.user)
            
            group_inv.accepted = True
            group_inv.save()
        else:
            group_inv.delete()

        return Response({f"{self.status}": True}, status=200) 


class DeleteGroupInvitation(AcceptGroupInvitation):
    status = "delete"


class JoinGroupWithCode(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            group = Group.objects.get(code=request.data["code"])
        except Group.DoesNotExist:
            return Response({"group_err": True}, status=400)

        user = User.objects.get(id=token_verification(request)) 
        group_member, created = GroupMember.objects.get_or_create(group=group, user=user)

        group_chatroom = GroupChatRoom.objects.get(group__id=group.id)

        if user not in group_chatroom.members.all():
            group_chatroom.members.add(user)

        return Response({"group": group.serialize()}, status=200)


# get random users that are not in specific group
class GetRandomUsersNotInGroup(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        group_chatroom = GroupChatRoom.objects.get(id=request.query_params["room_id"])
        number_per_page = request.query_params["number_per_page"]
        page = request.query_params["page"]
        
        if cache.get(f"random_users_not_in_group{group_chatroom.id}") is None:
            users = User.objects.all().order_by("-id")

            # user that's not in group
            not_in_group = []

            for user in users:
                if user not in group_chatroom.members.all():
                    not_in_group.append(user)
            
            cache.set(f"random_users_not_in_group{group_chatroom.id}", not_in_group, TEN_MINUTES_IN_SECONDS)
        else:
            not_in_group = cache.get(f"random_users_not_in_group{group_chatroom.id}")

        paginator = Paginator(not_in_group, per_page=number_per_page)
        random_users = paginator.get_page(page)
        random_users = sample(random_users, len(random_users))

        users_serialize = []

        for user in random_users:
            user_serialize = user.serialize()
            user_serialize["invited"] = False
            users_serialize.append(user_serialize)

        return Response({"random_users": users_serialize, "total_pages": paginator.num_pages}, status=200) 


class SearchUsersNotInGroup(APIView):
    permission_clases = [ IsAuthenticated ]

    def get(self, request):
        group_chatroom = GroupChatRoom.objects.get(id=request.query_params["room_id"])
        number_per_page = request.query_params["number_per_page"]
        page = request.query_params["page"]
        search_text = request.query_params["search_text"]

        users = User.objects.filter(username__icontains=search_text).exclude(id=token_verification(request)) 
        not_in_group = []

        for user in users:
            if user not in group_chatroom.members.all():
                not_in_group.append(user)
            
        paginator = Paginator(not_in_group, per_page=number_per_page)
        users = paginator.get_page(page)
        users_serialize = []

        for user in users:
            user_serialize = user.serialize()
            user_serialize["invited"] = False
            users_serialize.append(user_serialize)
        
        return Response({"users": users_serialize, "total_pages": paginator.num_pages}, status=200) 


class GroupDetail(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        try:
            group_chatroom = GroupChatRoom.objects.get(id=request.query_params["room_id"])
        except GroupChatRoom.DoesNotExist:
            return Response({"group_err": True}, status=400)

        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        if user not in group_chatroom.members.all():
            return Response({"not_in_group": True}, status=400)

        return Response({"group": group_chatroom.serialize()}, status=200)


class UpdateGroupDetail(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ parsers.MultiPartParser ]

    def post(self, request):
        try:
            group_chatroom = GroupChatRoom.objects.get(id=request.data["room_id"])
        except GroupChatRoom.DoesNotExist:
            return Response({"group_err": True}, status=400)

        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        if user not in group_chatroom.members.all():
            return Response({"not_in_group": True}, status=400)        

        group = group_chatroom.group
        group.name = request.data["name"]
        group.is_public = True if request.data["status"] == "Public" else False
        group.is_private = True if request.data["status"] == "Private" else False

        if isinstance(request.data["profile"], InMemoryUploadedFile):
            group.profile = request.data["profile"]

        group.save()

        return Response({"group": group.serialize()}, status=200)
 

class LeaveGroup(APIView):
    permission_clases = [ IsAuthenticated ]

    def post(self, request):
        try:
            group_chatroom = GroupChatRoom.objects.get(id=request.data["room_id"])
        except GroupChatRoom.DoesNotExist:
            return Response({"group_err": True}, status=400)

        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        if user not in group_chatroom.members.all():
            return Response({"not_in_group": True}, status=400)

        group_chatroom.members.remove(user) 

        try:
            group_member = GroupMember.objects.get(group__id=group_chatroom.group.id, user__id=user.id) 
        except GroupMember.DoesNotExist:
            return Response({"member_err": True}, status=400)

        group_member.delete()
        return Response({"left": True}, status=200)


class KickUserFromGroup(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            group_chatroom = GroupChatRoom.objects.get(id=request.data["room_id"])
        except GroupChatRoom.DoesNotExist:
            return Response({"group_err": True}, status=400)

        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)
        
        try:
            user_to_be_kicked = User.objects.get(id=request.data["user_to_be_kicked_id"])
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        # only group creator can kick users 
        if user.id != group_chatroom.group.creator.id:
            return Response({"permission_err": True}, status=400)

        if user_to_be_kicked in group_chatroom.members.all():
            group_chatroom.members.remove(user_to_be_kicked) 

        try:
            group_member = GroupMember.objects.get(group__id=group_chatroom.group.id, user__id=user_to_be_kicked.id) 
        except GroupMember.DoesNotExist:
            return Response({"member_err": True}, status=400)

        group_member.delete() 
        return Response({"kicked": True}, status=200)
