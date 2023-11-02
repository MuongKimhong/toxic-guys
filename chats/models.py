from django.db import models

from users.models import User, date_format, profile_url

'''
ChatRoom is for 2 users chatting together.

Group does not need chatroom, because group
itself act like a chatroom
'''


class ChatRoom(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name="member", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.serialize(),
            "member" : self.member.serialize(),
            "created_date": date_format(self.created_date)
        }


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models>CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models>CASCADE)
    text = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "chatroom_id": self.chatroom.id,
            "sender": self.sender.serialize(),
            "receiver": self.receiver.serialize(),
            "text" : self.text,
            "created_date": date_format(self.created_date)
        }


class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="message_images/")
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "message_id": self.message.id,
            "image": profile_url(self.image),
            "created_date": date_format(self.created_date)
        }
