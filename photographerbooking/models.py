from django.db import models
from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from photographer.models import photographer

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
    payment_status = models.CharField(max_length=100,default="pending")



class photographerBookingWithKhalti(models.Model):
    booking_id = models.AutoField(primary_key=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photographer = models.ForeignKey(photographer, on_delete=models.CASCADE)
    date = models.DateField()
    enddate = models.DateField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=100)
    pid = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
