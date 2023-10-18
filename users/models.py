from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

import uuid


def profile_url(profile):
    return f"{settings.FULL_DOMAIN_PATH}{profile.url}" if profile else ""


def date_format(date):
    return date.strftime("%d/%b/%Y - %I:%M %p")


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
            "profile_url" : profile_url(self.profile),
            "created_date": date_format(self.created_date),
            "accept_anonymous_message": self.accept_anonymous_message
        }


class UserConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(User, related_name="friend", on_delete=models.CASCADE) # friend
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.connection.username}"
    
    def serialize(self):
        return {
            "user": self.user.serialize(),
            "connection": self.connection.serialize(),
            "created_date": date_format(self.created_date)
        }


class AnonymousUser(models.Model):
    _id = models.CharField(max_length=20, blank=True) #uid
    username = models.CharField(max_length=100, unique=True)
    ip_address = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self._id} - {self.username} - {self.ip_address}"
    
    def generate_uid(self):
        uniqe_uid = str(uuid.uuid4())[:8]

        if AnonymousUser.objects.filter(_id=uniqe_uid).exists(): self.generate_uid()

        return uniqe_uid

    def save(self, *args, **kwargs):
        if self._id == "":
            self._id = self.generate_uid()
        
        super(AnonymousUser, self).save(*args, **kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "_id": self._id,
            "username": self.username,
            "ip_address": self.ip_address,
            "created_date": date_format(self.created_date)
        }
