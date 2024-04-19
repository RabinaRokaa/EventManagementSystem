from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.conf import settings
# from django.contrib.auth.models import User
class booking(models.Model): #making class
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    User = models.CharField(max_length=100, default='')
    Type = models.CharField(max_length=100, default='')
    Event_Type = models.CharField(max_length=100) #making field
    Name = models.CharField(max_length=100) #making field
    Location = models.CharField(max_length=100) #making field
    Capacity = models.CharField(max_length=100) #making field
    Description = models.CharField(max_length=100) #making field
    Decoration = models.CharField(max_length=100) #making field
    Photography = models.CharField(max_length=100) #making field
    #for adding editor in description in admin page
    Date = models.DateTimeField(default=timezone.now)
    EndDate = models.DateTimeField(default=timezone.now)
    Cost= models.IntegerField(default=0, null=True, blank=True)

# class book(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     venue = models.ForeignKey(Venues, on_delete=models.CASCADE)