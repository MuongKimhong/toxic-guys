from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import parsers
import random
import jwt

from users.models import *


TWENTY_MINUTES_IN_SECONDS = 20 * 60


def token_verification(request):
    token = str(request.META.get("HTTP_AUTHORIZATION"))[7:]
    decoded = jwt.decode(token, options={"verify_signature": False})
    user = User.objects.get(id=int(decoded.get('user_id')))
    return user.id


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

        if cache.get("random_users") is None:
            users = User.objects.all()
            random_users = random.sample(list(users), users.count())
            cache.set("random_users", random_users, TWENTY_MINUTES_IN_SECONDS)
        else:
            random_users = cache.get("random_users")

        paginator = Paginator(random_users, per_page=10)
        random_users = paginator.get_page(page)
        random_users = [user.serialize() for user in random_users]

        responses = {
            "random_users": random_users,
            "total_pages": paginator.num_pages
        }

        return Response(responses, status=200)


class SearchUser(APIView):
    permission_classes = [ IsAuthenticated ]
    accept_anonymous_message = False

    def get(self, request):
        search_text = request.query_params.get("search_text")
        paginator_page = request.query_params.get("page")

        if search_text is None:
            return Response({"results": []}, status=200)

        if self.accept_anonymous_message is True: 
            users = User.objects.filter(username__icontains=search_text, accept_anonymous_message=True)
        else:
            users = User.objects.filter(username__icontains=search_text)

        paginator = Paginator(list(users), per_page=10)
        results = paginator.get_page(paginator_page)
        results = [user.serialize() for user in results]

        return Response({"results": results, "total_pages": paginator.num_pages}, status=200)


class SearchUserAcceptAnonymousMessage(SearchUser):
    accept_anonymous_message = True


class SendUserConnectionRequest(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        # user to be connected with
        try:
            user_to_be_connected = User.objects.get(id=request.data["user_to_be_connected_id"])
        except User.DoesNotExist:
            return Response({"user_not_found": True}, status=400)

        user_connection = UserConnection.objects.get_or_create(
            user_id=token_verification(request), connection=user_to_be_connected
        )
        return Response({"request_sent": True}, status=200)


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

    # resposne to connection request
    def check_response_status(user_connection, request):
        if request.data["response"] == "accept":
            user_connection.is_accepted = True
            user_connection.save()
            return Response({"accepted": True}, status=200)
        elif request.data["response"] == "reject":
            user_connection.delete()
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
            return Response(("request_not_found": True), status=400)

        return self.check_response_status(user_connection, request)
