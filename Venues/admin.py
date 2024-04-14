from django.contrib import admin
from Venues.models import Venues,ImageFile

class VenueAdmin(admin.ModelAdmin):
    list_disp=('Name', 'Location', 'Type', 'Description', 'Capacity', 'Cost', 'Venue_image',)  #for showing title and description
#register model

class ImageFileAdmin(admin.ModelAdmin):
    list_disp=('id',)

admin.site.register( Venues, VenueAdmin) #after register you can see models in admin
admin.site.register( ImageFile, ImageFileAdmin)
