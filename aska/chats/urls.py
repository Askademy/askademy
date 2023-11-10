from django.urls import path

from .views import index, room


urlpatterns = [
    path("", index, name="chat-room"),
    path("private/<str:room_name>/", room, name="private-chat"),
]
