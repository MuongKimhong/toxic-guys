from django.db import models

from users.models import User, date_format, profile_url
from groups.models import Group


class ChatRoom(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name="member", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    _type = models.CharField(max_length=10, default="user")
    last_message_created_date = models.DateTimeField(blank=True, null=True) # use to sort chatroom in GetChatRoomList API
    last_message_text = models.TextField(blank=True)
    last_message_sender_name = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.serialize(),
            "member" : self.member.serialize(),
            "created_date": date_format(self.created_date),
            "total_messages": Message.objects.filter(chatroom__id=self.id).count(),
            "type": self._type,
            "last_message_text": self.last_message_text,
            "last_message_sender_name": self.last_message_sender_name
        }


class MessageImage(models.Model):
    image = models.ImageField(upload_to="message_images/")
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "image": profile_url(self.image),
            "created_date": date_format(self.created_date)
        }


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    images = models.ManyToManyField(MessageImage, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "chatroom_id": self.chatroom.id,
            "sender": self.sender.serialize(),
            "receiver": self.receiver.serialize(),
            "text" : self.text,
            "created_date": date_format(self.created_date),
            "images": [image.serialize() for image in self.images.all()],
        }


class GroupChatRoom(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    _type = models.CharField(max_length=10, default="group")
    last_message_created_date = models.DateTimeField(blank=True, null=True) # use to sort chatroom in GetChatRoomList API
    last_message_text = models.TextField(blank=True)
    last_message_sender_name = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "group": self.group.serialize(),
            "members": [member.serialize() for member in self.members.all()],
            "created_date": date_format(self.created_date),
            "type": self._type,
            "last_message_text": self.last_message_text,
            "last_message_sender_name": self.last_message_sender_name
        }


class GroupMessageImage(models.Model):
    image = models.ImageField(upload_to="group_messages/images/")
    created_date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "image": profile_url(self.image),
            "created_date": date_format(self.created_date)
        }


class GroupMessage(models.Model):
    group_chatroom = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(GroupMessageImage, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "group_chatroom_id": self.group_chatroom.id,
            "sender": self.sender.serialize(),
            "text": self.text,
            "created_date": date_format(self.created_date),
            "images": [image.serialize() for image in self.images.all()],
        }
