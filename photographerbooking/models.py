from django.db import models
from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from django.contrib.auth.models import User
class photographerbooking(models.Model): #making class
    User = models.CharField(max_length=100, default='')  
    #user = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=100) #making field
    username = models.CharField(max_length=100) #making field
    location = models.CharField(max_length=100) #making field
    capacity = models.CharField(max_length=100) #making field
    description = models.CharField(max_length=100) #making field
    decoration = models.CharField(max_length=100) #making field
    venue = models.CharField(max_length=100) #making field
    #for adding editor in description in admin page
    date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    cost= models.IntegerField(default=0, null=True, blank=True)
