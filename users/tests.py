from django.contrib.auth.hashers import make_password
from users.models import *


def create_dummy_users():
    users_to_create = 3000

    for i in range(users_to_create):
        print(f"Creating dummy user {i}")

        dummy_user = User.objects.create(
            username=f"user{i}",
            email=f"user{i}@gmail.com",
            password="Testing123"
        )
    
    print(f"Finished created {users_to_create} dummy users")
    