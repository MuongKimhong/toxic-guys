from django.urls import path
from users.views import *

urlpatterns = [
    path("sign-up/", SignUp.as_view()),
    path("sign-in/", SignIn.as_view())
]