from django.core.cache import cache
from users.models import User, UserConnection
import random
import jwt


TWENTY_MINUTES_IN_SECONDS = 20 * 60


# verify token to extract user id
def token_verification(request):
    token = str(request.META.get("HTTP_AUTHORIZATION"))[7:]
    decoded = jwt.decode(token, options={"verify_signature": False})
    user = User.objects.get(id=int(decoded.get('user_id')))
    return user.id


# check  if user is connected or not_connected or request pending
# used in GetRandomUser & SearchUser api
def check_connection_status(request, user):
    user_serialize = user.serialize()

    try:
        user_connection = UserConnection.objects.get(
            user__id=token_verification(request),
            connection__id=user.id
        )
        if user_connection.is_accepted is True:
            user_serialize["status"] = {"connected": True, "not_connected": False, "request_pending": False}
        else:
            user_serialize["status"] = {"connected": False, "not_connected": False, "request_pending": True}
    except UserConnection.DoesNotExist:
        user_serialize["status"] = {"connected": False, "not_connected": True, "request_pending": False}
        
    return user_serialize
