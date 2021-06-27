from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return str(self.id)
 

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message=models.TextField(unique=False,blank=False)
    subject=models.CharField(max_length=50)
    creationdate=models.DateTimeField(auto_now_add=True)
    unread=models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
    