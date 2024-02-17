from django.db import models
from django.db import models
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
class photographer(models.Model): #making class
    Username = models.CharField(max_length=100) #making field
    Phone_Number = models.IntegerField(null=True,default=None)
    Email = models.CharField(max_length=100) #making field
    
    Photography_type = models.CharField(max_length=200) #making field
    Event_type = models.CharField(max_length=200) #making field
    #for adding editor in description in admin page
    Cost= models.IntegerField(default=0, null=True, blank=True)
    #field for uploading image 
    Image=models.FileField(upload_to="photography/", max_length=250,null=True,default=None)
   