from django.db import models
from django.db import models
from django.db import models
from django.db import models
from Venues.models import Venues
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from django.conf import settings
class Checking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venues, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

   #message after booking
    def __str__(self):
        return f'{self.user} has booked {self.venue} from {self.check_in} to {self.check_out}'