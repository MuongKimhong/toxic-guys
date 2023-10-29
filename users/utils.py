from django.core.cache import cache
from users.models import User
import random
import jwt


TWENTY_MINUTES_IN_SECONDS = 20 * 60


def token_verification(request):
    token = str(request.META.get("HTTP_AUTHORIZATION"))[7:]
    decoded = jwt.decode(token, options={"verify_signature": False})
    user = User.objects.get(id=int(decoded.get('user_id')))
    return user.id


def create_random_users_cache(request):
    users = User.objects.all().exclude(id=token_verification(request))
    not_connected_users = []

    # we want to get only users that are not connected yet
    for user in users:
        user_serialize = user.serialize()
        try:
            user_connection = UserConnection.objects.get(
                id=token_verification(request), 
                connection__id=user.id,
                is_accepted=False
            )
            user_serialize["request_pending"] = True
        except UserConnection.DoesNotExist:
            user_serialize["request_pending"] = False
        
        not_connected_users.append(user_serialize)

    random_users = random.sample(not_connected_users, len(not_connected_users))
    cache.set("random_users", random_users, TWENTY_MINUTES_IN_SECONDS)
