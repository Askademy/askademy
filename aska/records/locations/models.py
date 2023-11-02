from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Region name")
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="District name")
    region = models.ForeignKey(Region, related_name="districts", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        unique_together = ["name", "region"]
