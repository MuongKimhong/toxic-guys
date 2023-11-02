from django.db import models

from users.models import User, date_format

'''
ChatRoom is for 2 users chatting together.

Group does not need chatroom, because group
itself act like a chatroom
'''


class ChatRoom(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete.models.CASCADE)
    member = models.ForeignKey(User, related_name="member", on_delete.models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "creator": self.creator.serialize(),
            "member" : self.member.serialize(),
            "created_date": date_format(self.created_date)
        }


class Message(models.Model):
    pass


class MessageImage(models.Model):
    pass
