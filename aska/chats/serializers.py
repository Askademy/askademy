from rest_framework import serializers
import random
from users.models import CustomUser
from chats.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source="message")
    sender_id = serializers.CharField(source="sender.id")
    class Meta:
        model = ChatMessage
        fields = ("content", "sender_id",)


class UserChatListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_username(self, user):
        return user.get_full_name()
    
    def get_messages(self, user):
        return []
    
    def get_status(self, user):
        return random.choice(("online", "offline"))
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.get_full_name(),
            "profile_picture": instance.profile_picture.url,
            "messages": [],
            "status": random.choice(["online", "offline"])
        }
    class Meta:
        model = CustomUser
        fields = ("id", "username", "profile_picture", "messages", "status")