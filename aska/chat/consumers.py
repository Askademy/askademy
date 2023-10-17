import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatMessage

from .serializers import ChatMessageSerializer
from records.models import CustomUser

class PrivateChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)
    
    @database_sync_to_async
    def get_messages(self):
        messages = ChatMessage.objects.filter(
            sender__id=self.current_user_id,
            thread_name=self.room_group_name
        )
        serializer = ChatMessageSerializer(messages, many=True)
        return serializer.data
    
    @database_sync_to_async
    def save_message(self, sender, message, thread_name):
        ChatMessage.objects.create(sender=sender, message=message, thread_name=thread_name)
    
    async def connect(self):
        self.current_user_id = self.scope["user"].id
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        if int(self.current_user_id) < int(self.other_user_id):
            self.room_name = f"{self.current_user_id}_{self.other_user_id}"
        else:
            self.room_name = f"chat_{self.other_user_id}_{self.current_user_id}"
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data["sender_id"]
        sender = await self.get_user(sender_id)

        await self.save_message(sender=sender, message=message, thread_name=self.room_group_name)

        messages = await self.get_messages()

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id,
            'messages': messages
        })

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event['sender_id']
        messages = event['messages']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'messages': messages
        }))

