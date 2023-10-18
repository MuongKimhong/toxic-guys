from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


def profile_url(profile):
    return f"{settings.FULL_DOMAIN_PATH}{profile.url}" if profile else ""


class User(AbstractUser):
    email = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True)
    accept_anonymous_message = models.BooleanField(default=False)
    profile = models.ImageField(upload_to="users_profiles/", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "profile" : profile_url(self.profile),
            "created_date": self.created_date.strftime("%d/%b/%Y - %I:%M %p")
        }