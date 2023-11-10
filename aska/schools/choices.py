from django.db import models
from django.utils.translation import gettext_lazy as _


class SchoolType(models.TextChoices):
    MIXED = "mixed", _("Mixed")
    MALES = "males", _("Males")
    FEMALES = "females", _("Females")


class SchoolOwner(models.TextChoices):
    PRIVATE = "private", _("Private")
    GOVERNMENT = "government", _("Government")
