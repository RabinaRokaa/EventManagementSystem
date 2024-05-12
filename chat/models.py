# models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    messaged_to = models.ForeignKey(User, related_name='messaged_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.messaged_to.username}: {self.message}'


