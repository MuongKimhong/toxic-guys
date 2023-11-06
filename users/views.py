from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView

from rest_framework import parsers
from random import sample
import random
import jwt

from users.models import *
from users.utils import token_verification, check_connection_status
from notifications.models import *
from notifications.views import send_notification
from chats.models import ChatRoom


TWENTY_MINUTES_IN_SECONDS = 20 * 60


# extract access token from http request
def extract_token(request):
    return str(request.META.get("HTTP_AUTHORIZATION"))[7:]


def check_password_strong(password):
    length_check       = False
    uppercase_check    = False

    if len(str(password)) >= 8: length_check = True
    
    # if string consists of one upper case
    for char in str(password):
        if char.isupper():
            uppercase_check = True
            break             

    return False if ((length_check is False) or (uppercase_check is False)) else True


def get_token(user):
    refresh_token = RefreshToken.for_user(user) 
    access_token  = refresh_token.access_token

    data = {
        'user': user.serialize(),
        'refresh_token': str(refresh_token),
        'access_token' : str(access_token)
    }
    return data


'''
All requests that required authentication
will perform tokens (access & refresg) change
via renew_token function
'''
def renew_token(request):
    user = User.objects.get(id=token_verification(request))

    token = extract_token(request)

    # blacklist old token
    try:
        bl_token = BlackListAccessToken.objects.get(access_token=token)
        return {"invalid_token": True}
    except BlackListAccessToken.DoesNotExist:
        bl_token = BlackListAccessToken.objects.create(access_token=token)

    return get_token(user)
    

class RenewAccessTokenWithRefreshToken(APIView):
    permission_classes = [ AllowAny ]

    def post(self, request):
        refresh_token = request.data["refresh_token"]
        decoded = jwt.decode(token, options={"verify_signature": False})
        try:
            user = User.objects.get(id=int(decoded.get("user_id")))
        except User.DoesNotExist:
            return Response({"error": True}, status=400)
        
        # blacklist old token
        try:
            bl_token = BlackListRefreshToken.objects.get(refresh_token=refresh_token)
            return Response({"invalid_token": True}, status=400)
        except BlackListRefreshToken.DoesNotExist:
            bl_token = BlackListRefreshToken.objects.create(refresh_token=refresh_token)
        
        return Response(get_token(user), status=200)


class SignUp(APIView):
    permission_classes = [ AllowAny ]

    def post(self, request):
        data = request.data

        if data["password"] != data["confirm_password"]:
            return Response({"two_password_not_match": True}, status=400)
        
        if User.objects.filter(email=data["email"]).exists() is True:
            return Response({"email_taken": True}, status=400)

        if User.objects.filter(username=data["username"]).exists() is True:
            return Response({"username_taken": True}, status=400)

        if check_password_strong(data["password"]) is False:
            return Response({"weak_password": "Password must contains 8 char and 1 uppercase"}, status=400)

        User.objects.create(
            email = data["email"],
            username = data["username"],
            password = make_password(data["password"])
        )
        return Response({"signup_success": True}, status=200)


class SignIn(APIView):
    permission_classes = [ AllowAny ]

    def post(self, request):
        try:
            user = User.objects.get(username=request.data["username"])
        except User.DoesNotExist:
            return Response({"error": True}, status=400)

        if check_password(request.data["password"], user.password) is False:
            return Response({"error": True}, status=400)

        return Response(get_token(user), status=200)


class SignOut(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        access_token = extract_token(request)
        refresh_token = request.data["refresh_token"]

        BlackListAccessToken.objects.get_or_create(access_token=access_token)
        BlackListRefreshToken.objects.get_or_create(refresh_token=refresh_token)

        return Response({"success": True}, status=200)


class ChangeUserProfile(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ parsers.MultiPartParser ]

    def post(self, request):
        profile = request.data["profile"]
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"error": True}, status=400)

        new_token = renew_token(request)
        if new_token.get("invalid_token"):
            return Response({"invalid_token": True}, status=400)

        user.profile = profile
        user.save()  
        return Response({"profile": user.serialize()['profile_url'], "new_token": new_token}, status=200)


class UpdateEmailAndUsername(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"error": True}, status=400)      

        new_token = renew_token(request)
        if new_token.get("invalid_token"):
            return Response({"invalid_token": True}, status=400)

        if user.email != request.data["email"]:
            if User.objects.filter(email=request.data["email"]).exists():
                return Response({"email_error": "Email is already taken"}, status=400)

        if user.username != request.data["username"]:
            if User.objects.filter(username=request.data["username"]).exists():
                return Response({"username_error": "Username is already taken"}, status=400)

        user.email = request.data["email"]
        user.username = request.data["username"]
        user.save()

        return Response({"success": True, "new_token": new_token}, status=200)


class ChangePassword(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"error": True}, status=400)
        
        if check_password(request.data["old_password"], user.password) is False:
            return Response({"old_password_error": "Incorrect old password"}, status=400)

        if check_password_strong(request.data["new_password"]) is False:
            return Response({"weak_password": "Password must contains 8 char and 1 uppercase"}, status=400)

        new_token = renew_token(request)
        if new_token.get("invalid_token"):
            return Response({"invalid_token": True}, status=400)

        user.password = make_password(request.data["new_password"])
        user.save()
        return Response({"success": True, "new_token": new_token}, status=200)


class GetRandomUsers(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        page = request.query_params.get("page")
        number_per_page = request.query_params.get("number_per_page")
        users = list(User.objects.all().exclude(id=token_verification(request)))

        random_users = sample(users, len(users))

        paginator = Paginator(random_users, per_page=number_per_page)
        random_users = paginator.get_page(page).object_list

        response = []

        # check if user is connected or not connected or request pending
        for user in random_users:
            response.append(check_connection_status(request, user))

        return Response({"random_users": response, "total_pages": paginator.num_pages}, status=200) 


class SearchUser(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        search_text = request.query_params.get("search_text")
        paginator_page = request.query_params.get("page")
        number_per_page = request.query_params.get("number_per_page")

        if search_text is None:
            return Response({"results": []}, status=200)

        users = User.objects.filter(username__icontains=search_text).exclude(id=token_verification(request)) 
        paginator = Paginator(list(users), per_page=number_per_page)
        results = paginator.get_page(paginator_page).object_list

        response = []
 
        # check if user is connected or not connected or request pending
        for user in results:
            response.append(check_connection_status(request, user))

        return Response({"results": response, "total_pages": paginator.num_pages}, status=200)


# search when user typing
class SearchUserAcceptAnonymousMessageOnTyping(APIView):
    permission_classes = [ AllowAny ]
    on_typing = True

    def get(self, request):
        search_text = request.query_params.get("search_text")

        if search_text is None:
            return Response({"results": []}, status=200)

        users = User.objects.filter(username__icontains=search_text, accept_anonymous_message=True)

        if self.on_typing is True:
            users = random.sample(list(users), users.count())
            # select only 10 users if query has more than 20 users
            if len(users) >= 20:
                users = users[:10]      

            results = [user.serialize() for user in users]
            return Response({"results": results}, status=200)
        else:
            page = request.query_params.get("page")
            paginator = Paginator(list(users), per_page=10)
            users = paginator.get_page(page)
 
            results = [user.serialize() for user in users]
            return Response({"results": results, "total_pages": paginator.num_pages}, status=200)


# search when Enter key press
class SearchUserAcceptAnonymousMessage(SearchUserAcceptAnonymousMessageOnTyping):
    on_typing = False


class SendUserConnectionRequest(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        user = User.objects.get(id=token_verification(request))

        # user to be connected with
        try:
            user_to_be_connected = User.objects.get(id=int(request.data["user_to_be_connected_id"]))
        except User.DoesNotExist:
            return Response({"user_not_found": True}, status=400)
  
        user_connection_for_user, created = UserConnection.objects.get_or_create(user=user, connection=user_to_be_connected)

        send_notification(
            sender=user, 
            receiver=user_to_be_connected, 
            text=f"{user.username} wants to connect with you"
        )
        return Response({"request_sent": True}, status=200)


class UnsendConnectionRequest(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        # user to be unconnected with
        try:
            user_to_be_unconnected = User.objects.get(id=int(request.data["user_to_be_unconnected_id"]))
        except User.DoesNotExist:
            return Response({"user_not_found": True}, status=400)

        '''
        if A unconnnect with B, Delete UserConnection object for both A & B 
        '''

        try:
            # utbu is user_to_be_unconnected
            user_connection_for_utbu = UserConnection.objects.get(
                user=user_to_be_unconnected, connection__id=token_verification(request)
            )
            user_connection_for_utbu.delete()
        except UserConnection.DoesNotExist:
            pass

        try:
            user_connection = UserConnection.objects.get(
                user_id=token_verification(request), connection=user_to_be_unconnected
            )
            user_connection.delete()

            try:
                notification = Notification.objects.get(sender__id=token_verification(request), receiver__id=user_to_be_unconnected.id)
                notification.delete()
            except Notification.DoesNotExist:
                pass

            return Response({"success": True}, status=200)
        except UserConnection.DoesNotExist:
            return Response({"connection_not_found": True}, status=400) 


class GetAllConnectionRequests(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user_connections = UserConnection.objects.filter(
            connection__id=token_verification(request), is_accepted=False, is_rejected=False
        )
        user_connections = [user_connection.serialize() for user_connection in user_connections.order_by("-id")]
        return Response({"connection_requests": user_connections}, status=200)


class AcceptOrRejectConnectionRequest(APIView):
    permission_classes = [ IsAuthenticated ]

    def delete_notification(self, request):
        if request.data.get("notification_id") is None:
            return None

        try:
            notification = Notification.objects.get(id=request.data.get("notification_id"))
            notification.delete()
        except Notification.DoesNotExist: 
            return None

    # when 2 users connected with each other, create a new chatroom for them    
    def create_chatroom(self, request):
        chatroom = ChatRoom.objects.create(
            creator_id=token_verification(request),
            member_id=request.data["request_sender_id"]
        )
        
    # resposne to connection request
    def check_response_status(self, user_connection, request):
        if request.data["response"] == "accept":
            user_connection.is_accepted = True
            user_connection.save()

            # if B accept the request, create UserConnection object for B with is_accepted=True 
            user_connection_for_accepter, created = UserConnection.objects.get_or_create(
                user=user_connection.connection, connection=user_connection.user, is_accepted=True
            )

            # send notification to request sender that request has been acccepted
            send_notification(
                user_connection.connection,
                user_connection.user,
                f"{user_connection.connection.username} has accepted your connection request",
                _type="connection-accept"
            )
            self.delete_notification(request) # delete connection request notification

            self.create_chatroom(request)

            return Response({"accepted": True}, status=200)
        elif request.data["response"] == "reject":
            user_connection.delete()

            self.delete_notification(request)

            return Response({"rejected": True}, status=200)
        else:
            return Response({"error": True}, status=400)

    def post(self, request):
        if (request.data.get("request_sender_id") is None) or (request.data.get("response") is None):
            return Response({"incorrect_param": True}, status=400)

        try:
            user_connection = UserConnection.objects.get(
                user__id=request.data["request_sender_id"],
                connection__id=token_verification(request)
            )
        except UserConnection.DoesNotExist:
            return Response({"request_not_found": True}, status=400)

        return self.check_response_status(user_connection, request)


# get all friends
class GetAllConnections(APIView):
    permission_classes = [ IsAuthenticated ]
    
    def get(self, request):
        try:
            user = User.objects.get(id=token_verification(request))
        except User.DoesNotExist:
            return Response({"error": True}, status=400)
        
        user_connections = UserConnection.objects.filter(user__id=user.id).order_by("-id")
        user_connections = [connection.serialize() for connection in user_connections]

        return Response({"connections": user_connections}, status=200)
