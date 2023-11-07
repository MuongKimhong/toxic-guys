from django.db import models

from users.models import User, date_format
from groups.models import GroupInvitation


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name="notification_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="notification_receiver", on_delete=models.CASCADE)
    _type = models.CharField(max_length=100, default="connection") # type of notification 
    text  = models.TextField()
    seen_by_receiver = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    # use to accept or delete group invitation in notification dashboard client
    group_invitation = models.ForeignKey(GroupInvitation, on_delete=models.CASCADE, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.serialize(),
            "receiver": self.receiver.serialize(),
            "type": self._type,
            "text": self.text,
            "seen_by_receiver": self.seen_by_receiver,
            "created_date": date_format(self.created_date),
            "group_invitation": self.group_invitation.serialize() if self.group_invitation else None
            # "group_invitation_id": self.group_invitation.id if self.group_invitation else None
        }
