from django.shortcuts import render, get_object_or_404

from users.models import CustomUser
from chats.serializers import UserChatListSerializer


def index(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    serializers = UserChatListSerializer(users, many=True)

    current_user = request.user
    context = {
        "users": serializers.data,
        "current_user": {
            "id": current_user.id,
            "username": current_user.get_full_name(),
            "profile_picture": current_user.profile_picture.url
        }
    }
    return render(request, "chat/index.html", context)

def room(request, room_name):
    user = get_object_or_404(CustomUser, id=room_name)
    context = {
        "room_name": room_name, 

    }
    return render(request, "chat/room.html", context=context)
