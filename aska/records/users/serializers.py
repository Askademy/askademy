from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError

from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate

from . import choices
from records.users.models import (
    CustomUser,
    UserSchool,
    Friendship,
    PasswordResetRequest,
)


class ForgotPasswordSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()
    send_to = serializers.ChoiceField(
        choices=choices.SEND_CODE_TO, label="Send code to"
    )

    def get_user(self):
        # Get the user using the given data
        phone_or_email = self.initial_data["phone_or_email"]
        try:
            return CustomUser.objects.get(
                Q(phone_number=phone_or_email) | Q(email=phone_or_email)
            )
        except:
            return None

    def validate_send_to(self, send_to):
        user = self.get_user()
        user_has_email = True if user and user.email else False
        if send_to == "email" and not user_has_email:
            raise serializers.ValidationError("The user has no email address")
        elif send_to == "phone" and not settings.CAN_SEND_SMS:
            raise serializers.ValidationError(
                "Sorry, we are not able to send sms. Please try other option"
            )
        return send_to

    def validate_phone_or_email(self, phone_or_email):
        try:
            user = CustomUser.objects.get(
                Q(phone_number=phone_or_email) | Q(email=phone_or_email)
            )
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "User with this phone number or email does not exist."
            )
        return user

    def create_password_reset_request(self):
        """Create a password reset request for the user"""
        user = self.validated_data["phone_or_email"]
        PasswordResetRequest.objects.filter(user=user).delete()
        reset_request = PasswordResetRequest.objects.create(user=user)
        return reset_request


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Retrieve user from kwargs
        super().__init__(*args, **kwargs)

    def validate_code(self, code):
        try:
            reset_request = PasswordResetRequest.objects.get(user=self.user, code=code)
        except PasswordResetRequest.DoesNotExist:
            raise serializers.ValidationError("Invalid reset code.")
        if not reset_request.is_valid():
            raise serializers.ValidationError("Reset code has expired.")
        return code

    def validate_confirm_password(self, value):
        if self.initial_data["new_password"] != value:
            raise serializers.ValidationError("Passwords don't match.")
        return value

    def save(self):
        password = self.validated_data["new_password"]
        self.user.set_password(password)
        self.user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, old_password):
        user = self.context["request"].user
        if not authenticate(phone_number=user.phone_number, password=old_password):
            raise ValidationError("Incorrect password")
        return old_password

    def to_representation(self, instance):
        return {"message": "Password changed"}

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data["new_password"])
        user.save()
        return {"message": "Password changed"}


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            message = "Unable to log in with provided credentials."
            raise serializers.ValidationError(
                detail={"detail": message}, code="authorization"
            )
        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        user = instance["user"]
        token, created = Token.objects.get_or_create(user=user)
        return {**user.get_info(), "token": token.key}

class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="get_full_name")
    schools = serializers.SerializerMethodField("get_schools")
    level = serializers.ChoiceField(choices=choices.LEVEL, allow_blank=True)
    friendship = serializers.SerializerMethodField()

    @property
    def user(self):
        return self.context["request"].user

    @property
    def action(self):
        return self.context["view"].action

    @property
    def request(self):
        return self.context["request"]

    def get_friendship(self, instance):
        if self.user.is_authenticated:
            return self.user.get_friendship_status(instance)
        return None

    def get_schools(self, user):
        schools = user.schools.all()
        if user.schools:
            return [sch.school.name for sch in schools]
        return None

    def get_fields(self):
        fields = super().get_fields()
        if self.action == "create":
            fields.pop("is_active")
        elif self.action == "update":
            fields.pop("password")
        return fields

    def to_representation(self, user):
        action = self.action
        if action in ("update", "retrieve"):
            return super().to_representation(user)
        else:
            data = user.get_info()
            if action == "create":
                token = Token.objects.create(user=user)
                return {**data, "token": token.key}
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "nickname",
            "username",
            "email",
            "phone_number",
            "birthdate",
            "gender",
            "bio",
            "friendship",
            "profile_picture",
            "cover_picture",
            "schools",
            "subjects",
            "level",
            "points",
            "date_joined",
            "is_active",
            "last_login",
            "password",
        )
        model = CustomUser
        extra_kwargs = {
            "password": {"write_only": True},
            "points": {"read_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }


class UserSchoolSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = UserSchool
        fields = ["school", "date_started", "date_completed", "present"]



class FriendshipSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    status = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField(source='timestamp')
    user_profile_url = serializers.SerializerMethodField()
    request_url = serializers.SerializerMethodField()

    def get_username(self, obj):
        user = self.get_user(obj)
        return user.get_full_name()

    def get_sender(self, obj):
        user = self.get_user(obj)
        return user == obj.receiver

    def get_user_profile_url(self, obj):
        user = self.get_user(obj)
        return user.get_api_abs_url()

    def get_request_url(self, obj):
        user = self.get_user(obj)
        return user.get_api_abs_url() + "friend_request/"

    def get_user(self, obj):
        request_user = self.context["request"].user
        return obj.receiver if obj.sender == request_user else obj.sender

    class Meta:
        model = Friendship
        fields = ["username", "sender", "status", "time", "user_profile_url", "request_url"]
