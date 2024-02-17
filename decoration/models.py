from django.db import models
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
class decoration(models.Model): #making class
    Booking_id = models.IntegerField(default=0, null=True, blank=True)
    Name = models.CharField(max_length=100) #making field
    Type = models.CharField(max_length=100) #making field
    Description = models.CharField(max_length=200) #making field
    #for adding editor in description in admin page
    Cost= models.IntegerField(default=0, null=True, blank=True)
    #field for uploading image 
    Decoration_image=models.FileField(upload_to="decoration/", max_length=250,null=True,default=None)
   