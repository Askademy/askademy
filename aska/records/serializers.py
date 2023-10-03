from rest_framework import serializers

from .others import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ("receiver", )