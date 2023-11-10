import os
from django.core.files import File
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .choices import RequestStatus
from .models import CustomUser, UserPrivacySettings, Friendship, Notification
from utils.helpers.image_processing import create_text_image 


# Generate profile picture when a new CustomUser is created
@receiver(post_save, sender=CustomUser)
def generate_profile_picture(sender, instance, created, **kwargs):
    if created and not instance.profile_picture:
        # Generate profile picture using user's initials
        initials = instance.first_name[0] + instance.last_name[0]
        image_path = create_text_image(initials, 150, 150)

        # Save generated image to profile_picture field
        with open(image_path, "rb") as f:
            file_name = f"{instance.phone_number}.png"
            instance.profile_picture.save(file_name, File(f), save=True)
        
        # Delete the generated image
        os.remove(image_path)


# Create UserPrivacySettings when a new CustomUser is created
@receiver(post_save, sender=CustomUser)
def create_user_privacy_settings(sender, instance, created, **kwargs):
    if created:
        UserPrivacySettings.objects.create(user=instance)


# Send notification to user if friend request is sent, received or declined
@receiver(post_save, sender=Friendship)
def friendship_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            receiver=instance.receiver,
            message=f"{instance.sender.get_full_name()} sent you friend request."
        )
    print(instance.status == RequestStatus.ACCEPTED,)

    if instance.status == RequestStatus.ACCEPTED:
        Notification.objects.get_or_create(
            receiver=instance.sender,
            message=f"{instance.receiver.get_full_name()} has accepted your friend request"
        )
        
    if instance.status == RequestStatus.DECLINED:
        Notification.objects.get_or_create(
            receiver=instance.sender,
            message=f"{instance.receiver.get_full_name()} has rejected your friend request"
        )


