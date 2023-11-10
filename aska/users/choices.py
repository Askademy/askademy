from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class SendCodeTo(models.TextChoices):
    PHONE_NUMBER = "phone", _("Phone number")
    EMAIL_ADDRESS  = "email", _("Email address")


class GradeLevel(models.TextChoices):
    UPPER_PRIMARY = "UPP", _("Upper Primary")
    JUNIOR_HIGH = "JHS", _("Junior High")
    SENIOR_HIGH = "SHS", _("Senior High")


class RequestStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    DECLINED = "declined", _("Declineed")
