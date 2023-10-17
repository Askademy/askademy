from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/private/(?P<user_id>\w+)/$", consumers.PrivateChatConsumer.as_asgi()),
]