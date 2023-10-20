from django.contrib.auth.hashers import make_password
from users.models import *


def create_dummy_users():
    for i in range(300):
        print(f"Creating dummy user {i}")

        dummy_user = User.objects.create(
            username=f"user{i}",
            email=f"user{i}@gmail.com",
            password=make_password("Testing123")
        )
    
    print("Finished created 300 dummy users")
    