from notifications.models import Notification


def send_notification_request(sender, receiver, text, _type=None):

    notification = Notification.objects.get_or_create(
        sender = sender,
        receiver = receiver,
        text = text
    )
    if _type is not None:
        notification._type = _type
        notification.save()
