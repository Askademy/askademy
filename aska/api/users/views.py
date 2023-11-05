from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import viewsets, status, views


from django.contrib import auth
from django.db.models import Q
from django.contrib.auth import logout, login
from django.shortcuts import get_object_or_404, redirect

from utils.helpers.verifications import send_verification_code_to_user

from .permissions import IsAuthenticated, UserProfilePermission
from .filters import CustomUserFilter

from records.others import Notification
from records.users.models import (
    Friendship,
    CustomUser,
    UserSchool,
)
from records.users.serializers import (
    RegisterUserSerializer,
    UserSerializer,
    UserSchoolSerializer,
    FriendshipSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from rest_framework.serializers import Serializer
from records.serializers import NotificationSerializer
from records.feeds.serializers import PostSerializer


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = Serializer

    def list(self, request):
        abs_url = request.build_absolute_uri
        return Response({
            "register": abs_url(reverse("api:auth-register-user")),
            "login": abs_url(reverse("api:auth-login")),
            "logout": abs_url(reverse("api:auth-logout")),
            "change Password": abs_url(reverse("api:auth-change-password")),
            "Forgot Password": abs_url(reverse("api:auth-forgot-password"))
        })
    
    @action(detail=False, methods=["post"], serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(
            {"detail": "You have logout successfully"},
            status=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=["post"], serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        auth.login(request, request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path="forgot-password", serializer_class=ForgotPasswordSerializer)
    def forgot_password(self, request):
        if request.user.is_authenticated:
            return Response({"message": "You are already authenticated. The 'Forgot Password' functionality is only available to users who need to reset their password"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Do something with the validated serializer data, such as send a password reset email
        reset_request = serializer.create_password_reset_request()
        send_to = serializer.validated_data["send_to"]
        send_verification_code_to_user(request=request, password_reset_request=reset_request, send_to=send_to)
        url = reverse("api:auth-reset-password", kwargs={"user_id": reset_request.user.pk})
        return Response(status=status.HTTP_302_FOUND, headers={"Location": url})

    @action(detail=False, methods=["post"], url_path=r"(?P<user_id>[^/.]+)/reset-password", serializer_class=ResetPasswordSerializer)
    def reset_password(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = ResetPasswordSerializer(data=request.data, user=user)
        serializer.is_valid(raise_exception=True)
        login(request, user)
        return Response({"message": "Password reset successful. You can now use your new password to log in."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="register", serializer_class=RegisterUserSerializer)
    def register_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [UserProfilePermission]
    serializer_class = UserSerializer
    filterset_class = CustomUserFilter
    lookup_field = "pk"

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action in ("update", "retrieve", "partial_update"):
            kwargs.setdefault("all_fields", True)
        return serializer_class(*args, **kwargs)

    @action(detail=True, serializer_class=PostSerializer)
    def posts(self, request, *args, **kwargs):
        user = self.get_object()
        posts = user.posts.all()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, serializer_class=NotificationSerializer)
    def notifications(self, request, *args, **kwargs):
        user = self.get_object()
        notifs = user.notifications.all()
        serializer = self.get_serializer(notifs, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=["get", "post"], serializer_class=UserSchoolSerializer)
    def schools(self, request, *args, **kwargs):
        if request.method == "POST":
            return super().create(request, *args, **kwargs)
        user_schools = UserSchool.objects.filter(user=self.get_object())
        serializer = self.get_serializer(user_schools, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def friends(self, *args, **kwargs):
        friends = self.get_object().get_friends()
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get", "post", "put", "delete"],
        serializer_class=FriendshipSerializer,
    )
    def friend_request(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj and request.method=="GET":
            pending_requests = Friendship.objects.filter(Q(sender=request.user) | Q(receiver=request.user) & ~Q(status="accepted"))
            serializer = FriendshipSerializer(pending_requests, many=True, context={"request": request})
            return Response(serializer.data)
        try:
            friendship = Friendship.objects.get(Q(sender=obj, receiver=request.user)|Q(receiver=obj, sender=request.user))
        except Friendship.DoesNotExist:
            if request.method == "POST":
                friendship = Friendship.objects.create(sender=request.user, receiver=obj)
            else:
                return Response("You are not friends")
        if request.method in ("PUT", "POST"):
            if friendship.receiver == request.user:
                friendship.status = "accepted"
                friendship.save()
        elif request.method == "DELETE":
            friendship.delete()
            return Response("Friend request deleted")
        serializer = self.get_serializer(friendship)
        
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def suggested_friends(self, *args, **kwargs):
        suggested_users = self.get_object().get_suggested_friends()
        serializer = self.get_serializer(suggested_users, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def level_mates(self, *args, **kwargs):
        mates = self.get_object().get_level_mates()
        serializer = self.get_serializer(mates, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def school_mates(self, *args, **kwargs):
        mates = self.get_object().get_school_mates()
        serializer = self.get_serializer(mates, many=True)
        return Response(serializer.data)

    
    