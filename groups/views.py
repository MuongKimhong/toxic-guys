from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers


from groups.models import Group, GroupInvitation, GroupMember
from chats.models import GroupChatRoom
from users.models import User
from users.utils import token_verification


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
        group_chatroom = GroupChatRoom.objects.create(group=group)
        group_chatroom.members.add(user)
        return Response({"group_created": True}, status=200)


class InviteUserToJoinGroup(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            group = Group.objects.get(id=request.data["group"])
        except Group.DoesNotExist:
            return Response({"group_err": True}, status=400)
        
        try:
            user = User.objects.get(id=request.data["user_to_be_invited"])
        except User.DoesNotExist:
            return Response({"user_err": True}, status=400)

        group_invitation = GroupInvitation.objects.get_or_create(group=group, user=user, inviter_id=token_verification(request))
        return Response({"invitation_sent": group_invitation.serialize()}, status=200)
