from django.db import models

from .choices import SchoolOwner, SchoolType
from users.models import CustomUser, Telephone



class School(models.Model):
    added_by = models.ForeignKey(
        CustomUser,
        related_name="schools_added",
        on_delete=models.SET_NULL,
        editable=False,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    owner = models.CharField(choices=SchoolOwner.choices, max_length=50, default="government")
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=SchoolType.choices, default="mixed")
    telephone = models.ForeignKey(Telephone,on_delete=models.SET_NULL,null=True,blank=True)
    district = models.ForeignKey("locations.District", on_delete=models.CASCADE)
    town = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=100, null=True, blank=True)
    location = models.URLField(null=True, blank=True, help_text="School location on google map")
    description = models.TextField(blank=True, null=True)
    date_established = models.DateField(blank=True, null=True)
    visible = models.BooleanField(default=True, help_text="Tick to show that the school is visible to users")
    logo = models.ImageField(upload_to="school", default="defaults/cover.jpeg")

    def get_school_info(self):
        """Returns a dictionary containing relevant information about the school."""
        school_info = {
            "name": self.name,
            "owner": self.get_owner_display(),
            "telephone": self.telephone and self.telephone.number,
            "address": f"{self.town}, {self.district.get_region_display()}",
            "logo": self.logo.url,
        }
        return school_info

    def old_students(self):
        """Return the users who have completed the school"""

    def current_students(self):
        """Return the students who are present in the school"""

    def __str__(self):
        return self.name


class SchoolPicture(models.Model):
    school = models.ForeignKey(
        School, related_name="pictures", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="school/images")
    caption = models.CharField(max_length=225)
    timestamp = models.DateTimeField(auto_now=True)


class SchoolFeed(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to="school/feeds", blank=True, null=True)
    school = models.ForeignKey(School, related_name="feeds", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, editable=False)
