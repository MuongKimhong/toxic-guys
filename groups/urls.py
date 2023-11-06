from django.urls import path
from groups.views import *

urlpatterns = [
    path("create-group/", CreateGroup.as_view()),
    path("invite-user-to-join-group/", InviteUserToJoinGroup.as_view()),
    path("accept-group-invitation/", AcceptGroupInvitation.as_view()),
    path("delete-group-invitation/", DeleteGroupInvitation.as_view()),
    path("join-group-with-code/", JoinGroupWithCode.as_view()),
    path('get-users-not-in-group/', GetRandomUsersNotInGroup.as_view()),
    path("group-detail/", GroupDetail.as_view()),
    path("update-group-detail/", UpdateGroupDetail.as_view()),
    path("leave-group/", LeaveGroup.as_view()),
]