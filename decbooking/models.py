from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from django.contrib.auth.models import User
class decbooking(models.Model): #making class
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    User = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100) #making field
    description = models.CharField(max_length=100) #making field
    date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    cost= models.IntegerField(default=0, null=True, blank=True)
