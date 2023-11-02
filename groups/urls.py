from django.urls import path
from groups.views import *

urlpatterns = [
    path("create-group/", CreateGroup.as_view())
]