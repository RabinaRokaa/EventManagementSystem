from django.db import models

from django.contrib.auth.models import User
from django.db import models

class profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your additional fields here, for example:
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username

