from django.urls import path
from users.views import *

urlpatterns = [
    path("sign-up/", SignUp.as_view()),
    path("sign-in/", SignIn.as_view()),
    path("sign-out/", SignOut.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("change-profile/", ChangeUserProfile.as_view()),
    path("update-email-username/", UpdateEmailAndUsername.as_view()),

    path("get-random-users/", GetRandomUsers.as_view()),
    path("search-users/", SearchUser.as_view()),
    path("search-users-accept-anonymous-message-on-typing/", SearchUserAcceptAnonymousMessageOnTyping.as_view()),
    path("search-users-accept-anonymous-message/", SearchUserAcceptAnonymousMessage.as_view()),
    path("send-user-connection-request/", SendUserConnectionRequest.as_view()),
    path("unsend-user-connection-request/", UnsendConnectionRequest.as_view()),
    path("get-all-connection-requests/", GetAllConnectionRequests.as_view()),
    path("accept-or-reject-connection-request/", AcceptOrRejectConnectionRequest.as_view()),
]