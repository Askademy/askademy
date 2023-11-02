from django.db import models
from records.users.models import CustomUser

class Telephone(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.number
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Notification(models.Model):
    receiver = models.ForeignKey(CustomUser, related_name="notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)