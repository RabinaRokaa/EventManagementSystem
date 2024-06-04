from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
class Venues(models.Model): #making class
    Name = models.CharField(max_length=100) #making field
    Location = models.CharField(max_length=100) #making field
    Type = models.CharField(max_length=100,null=True,default=None) #making field
    Description = models.CharField(max_length=200) #making field
    Capacity = models.IntegerField(default=0, null=True, blank=True)
    Cost= models.IntegerField(default=0, null=True, blank=True)
    #field for uploading image 
    # Venue_image=models.ImageField(upload_to="venues/", max_length=250,null=True,default=None)
    Venue_image = models.ManyToManyField('ImageFile')


class ImageFile(models.Model):
    image = models.ImageField(upload_to='venues/')

    # <div class="pictures">
    #                                         ${venue.Venue_image && venue.Venue_image.length > 0 ?
    #                                             `<div class="img"> 
    #                                                 <img src="${venue.Venue_image[0].image.url}" alt="${venue.Name}" width="300" height="150">
    #                                             </div>` : ''}
    #                                     </div> 

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.CharField(max_length=200)
    rating=models.IntegerField()
    venue_name=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
