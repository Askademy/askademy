from django.shortcuts import render, get_object_or_404

from records.models import CustomUser


def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    user = get_object_or_404(CustomUser, id=room_name)
    return render(request, "chat/room.html", {"room_name": room_name})
