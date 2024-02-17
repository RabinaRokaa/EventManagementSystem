from django.db import models
from django.db import models
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
class booking(models.Model): #making class
    Booking_id = models.IntegerField(default=0, null=True, blank=True)

    Event_Type = models.CharField(max_length=100) #making field
    Name = models.CharField(max_length=100) #making field
    Location = models.CharField(max_length=100) #making field
    Capacity = models.CharField(max_length=100) #making field
    Description = models.CharField(max_length=100) #making field
    Decoration = models.CharField(max_length=100) #making field
    Photography = models.CharField(max_length=100) #making field
    #for adding editor in description in admin page
    Date = models.DateTimeField()
    Cost= models.IntegerField(default=0, null=True, blank=True)
    #field for uploading image 
    Image=models.FileField(upload_to="decoration/", max_length=250,null=True,default=None)
   
