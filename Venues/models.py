from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
class Venues(models.Model): #making class
    Name = models.CharField(max_length=100) #making field
    Location = models.CharField(max_length=100) #making field
    Type = models.CharField(max_length=100,null=True,default=None) #making field
    Description = models.CharField(max_length=200) #making field
    #for adding editor in description in admin page
    # Description=HTMLField()  

    Capacity = models.IntegerField(default=0, null=True, blank=True)
    Cost= models.IntegerField(default=0, null=True, blank=True)
    #field for uploading image 
    Venue_image=models.FileField(upload_to="venues/", max_length=250,null=True,default=None)
    