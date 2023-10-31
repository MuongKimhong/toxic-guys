from django.core.cache import cache
from users.models import User, UserConnection
import random
import jwt


TWENTY_MINUTES_IN_SECONDS = 20 * 60


def token_verification(request):
    token = str(request.META.get("HTTP_AUTHORIZATION"))[7:]
    decoded = jwt.decode(token, options={"verify_signature": False})
    user = User.objects.get(id=int(decoded.get('user_id')))
    return user.id
