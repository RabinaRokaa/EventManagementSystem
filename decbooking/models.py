from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decoration.models import decoration

# from django.contrib.auth.models import User
class decbooking(models.Model): #making class
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    User = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100) #making field
    description = models.CharField(max_length=100) #making field
    date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    cost= models.IntegerField(default=0, null=True, blank=True)



class decorationBookingWithKhalti(models.Model):
    booking_id = models.AutoField(primary_key=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decoration = models.ForeignKey(decoration, on_delete=models.CASCADE)
    date = models.DateField()
    enddate = models.DateField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=100)
    pid = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
