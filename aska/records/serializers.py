from records.curriculums.serializers import *
from records.assessments.serializers import *
from records.feeds.serializers import *
from records.schools.serializers import *
from records.users.serializers import *

from rest_framework import serializers
from .others import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ("receiver", )