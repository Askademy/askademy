from django.db import models

from .import choices

class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(choices=choices.REGION, max_length=100)

    def __str__(self):
        return self.name
