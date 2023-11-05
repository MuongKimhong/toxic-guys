from django.urls import path
from groups.views import *

urlpatterns = [
    path("create-group/", CreateGroup.as_view()),
    path("invite-user-to-join-group/", InviteUserToJoinGroup.as_view()),
    path("accept-group-invitation/", AcceptGroupInvitation.as_view()),
    path("delete-group-invitation/", DeleteGroupInvitation.as_view()),
    path("join-group-with-code/", JoinGroupWithCode.as_view())
]