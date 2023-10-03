from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Friendship, Notification

@receiver(post_save, sender=Friendship)
def friendship_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            receiver=instance.receiver,
            message=f"{instance.sender.get_full_name()} sent you friend request."
        )
    elif instance.status == "accepted":
        Notification.objects.create(
            receiver=instance.sender,
            message=f"{instance.receiver.get_full_name()} has accepted your friend request"
        )
    elif instance.status == "declined":
        Notification.objects.create(
            receiver=instance.sender,
            message=f"{instance.receiver.get_full_name()} has rejected your friend request"
        )

