from django.contrib import admin
from Venues.models import Venues

class VenueAdmin(admin.ModelAdmin):
    list_disp=('Name', 'Location', 'Type', 'Description', 'Capacity', 'Cost', 'Venue_image',)  #for showing title and description
#register model
admin.site.register( Venues, VenueAdmin) #after register you can see models in admin

