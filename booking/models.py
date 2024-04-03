from django.db import models
from django.db import models
from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.conf import settings
class booking(models.Model): #making class
    Event_Type = models.CharField(max_length=100) #making field
    Name = models.CharField(max_length=100) #making field
    Location = models.CharField(max_length=100) #making field
    Capacity = models.CharField(max_length=100) #making field
    Description = models.CharField(max_length=100) #making field
    Decoration = models.CharField(max_length=100) #making field
    Photography = models.CharField(max_length=100) #making field
    #for adding editor in description in admin page
    # Date = models.DateTimeField(default=timezone.now)
    # EndDate = models.DateTimeField(timezone.now() + timezone.timedelta(days=1))
    Cost= models.IntegerField(default=0, null=True, blank=True)

# class book(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     venue = models.ForeignKey(Venues, on_delete=models.CASCADE)