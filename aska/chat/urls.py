from django.urls import path

from .views import index, room

app_name = "chat"

urlpatterns = [
    path("", index, name="home"),
    path("private/<str:room_name>/", room, name="private-chat"),
]
