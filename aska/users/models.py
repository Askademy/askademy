import random
from itertools import chain

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from .choices import Gender, GradeLevel, RequestStatus
from .managers import CustomUserManager
from curriculums.models import Subject


class Telephone(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.number


class PasswordResetRequest(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=100, default=str(random.randint(100000, 999999)), editable=False)

    def is_valid(self):
        # Check if the reset request is valid
        now = timezone.now()
        time_difference = now - self.timestamp
        return time_difference.total_seconds() < 300  # 5 minutes


class UserPrivacySettings(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name="privacy_settings")
    is_phone_number_public = models.BooleanField(default=False)
    is_birthdate_public = models.BooleanField(default=False)
    is_gender_public = models.BooleanField(default=False)
    is_email_public = models.BooleanField(default=False)


class CustomUser(AbstractUser):
    # Phone number field to use as the unique identifier of the user
    username = None
    nickname = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=Gender.choices, max_length=20)
    birthdate = models.DateField()
    bio = models.TextField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=100, choices=GradeLevel.choices, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="users", blank=True)
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to="users", blank=True, null=True)
    cover_picture = models.ImageField(upload_to="users", blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "first_name",
        "middle_name",
        "last_name",
        "gender",
        "birthdate",
    ]

    objects = CustomUserManager()

    def get_full_name(self):
        """Combine first, middle, and last name to create full name"""
        names = (self.first_name, self.middle_name, self.last_name)
        return " ".join((name for name in names if name))

    def get_info(self, app_name="api"):
        """
        Returns a dictionary of user information, including id, full name,
        profile picture URL and profile URL.
        """
        return {
            "id": self.id,
            "username": self.get_full_name(),
            "profile_picture": reverse("media", args=[self.profile_picture.url]) if self.profile_picture else None,
            "profile_url": reverse(f"{app_name}:users-detail", args=[self.pk])
        }

    def get_current_school(self):
        """Return the school in which ther user is currently attending"""
        return self.schools.first()

    def get_friends(self):
        """Return the user's friends"""
        friendship = Friendship.objects.filter(
            models.Q(sender=self) | models.Q(receiver=self),
            status="accepted",
        )
        related_user_ids = list(chain.from_iterable(friendship.values_list("sender", "receiver")))
        return self.__class__.objects.filter(id__in=related_user_ids).exclude(id=self.id)

    def get_suggested_friends(self):
        # Fetch friendships where the current user is either the sender or receiver
        friendship = Friendship.objects.filter(models.Q(sender=self) | models.Q(receiver=self))
        
        # Extract user IDs from the sender and receiver fields in the friendships
        related_user_ids = list(chain.from_iterable(friendship.values_list("sender", "receiver")))
        
        # Exclude the current user and users already in friendships from the suggested friends
        return self.__class__.objects.exclude(id__in=related_user_ids).exclude(id=self.id)


    def get_level_mates(self):
        """Return the user's level mates"""
        return self.__class__.objects.filter(level=self.level).exclude(id=self.id)

    def get_school_mates(self):
        """Return the user's school mates"""
        user_schools = UserSchool.objects.filter(user=self)
        schools_ids = list(user_schools.values_list("school", flat=True))
        users_schools = UserSchool.objects.filter(school__id__in=schools_ids)
        users_id = list(users_schools.values_list("user", flat=True))
        return self.__class__.objects.filter(id__in=users_id).exclude(id=self.id)

    def get_api_abs_url(self):
        """Return the api detail view for the user"""
        return reverse("api:users-detail", kwargs={"pk": self.pk})

    def get_web_abs_url(self):
        """Return the web detail view for the user"""
        return reverse("web:users-detail", kwargs={"pk": self.pk})    



    def _get_friendship(self, user):
        """Return the friendship object of the given user"""
        try:
            return Friendship.objects.get(
                models.Q(sender=self, receiver=user)
                | models.Q(receiver=self, sender=user)
            )
        except Friendship.DoesNotExist:
            return None

    def get_friendship_status(self, user):
        """Get the friendship status with the given user"""
        friendship = self._get_friendship(user)
        if not friendship:
            return None
        elif friendship.status == Friendship.ACCEPTED:
            return Friendship.ACCEPTED
        elif friendship.sender == self:
            return Friendship.SENT
        elif friendship.receiver == self:
            return Friendship.RECEIVED

    def request_password_reset_code(self):
        """Return password reset request that can be used to reset password"""
        request, created = PasswordResetRequest.objects.get_or_create(user=self)
        if not created:
            return "You have already requested password reset code. Wait for some time to request new code Or use the code you already have to reset your password"
        return request.code

    def __str__(self):
        return f"{self.first_name} ({self.id})"


class Friendship(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_friend_requests")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_friend_requests")
    status = models.CharField(max_length=10, choices=RequestStatus.choices, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    SENT = "sent"
    ACCEPTED = "accepted"
    RECEIVED = "received"

    def __str__(self):
        return f"{self.sender.first_name} {self.sender.id} -->> {self.receiver.first_name} {self.receiver.id}"


class UserSchool(models.Model):
    user = models.ForeignKey(CustomUser, related_name="schools", on_delete=models.CASCADE)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE)
    date_started = models.DateField(blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)
    present = models.BooleanField()

    def __str__(self):
        return f"{self.user.first_name} {self.school.name}"


class Notification(models.Model):
    receiver = models.ForeignKey(CustomUser, related_name="notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)