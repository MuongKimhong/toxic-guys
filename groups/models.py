from django.db import models

from users.models import User, profile_url, date_format

import random
import string


class Group(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    profile = models.ImageField(upload_to="groups_profiles/", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"Group {self.id} - {self.name}"
    
    def generate_code(self):
        CODE_LENGTH = 7
        code = ''.join(random.choices(string.ascii_lowercase, k=CODE_LENGTH))

        if Group.objects.filter(code=code).exists(): self.generate_code()

        return code

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = self.generate_code()
        
        super(Group, self).save(*args, **kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "profile": profile_url(self.profile),
            "created_date": date_format(self.created_date),
            "creator": self.creator.serialize(),
            "is_public": self.is_public,
            "is_private": self.is_private
        }


class GroupMember(models.Model):
    group = models.ForeignKey(Group, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return f"{self.group.name} - user: {self.user.username}"

    def serialize(self):
        return {
            "group_id": self.group.id,
            "group_code": self.group.code,
            "user": self.user.serialize()
        }
