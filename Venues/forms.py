# forms.py
from django import forms
from .models import Venues

class VenuesForm(forms.ModelForm):
    
    class Meta:
        model = Venues
        fields = [ 'Name', 'Location', 'Type', 'Description', 'Capacity', 'Cost', 'Venue_image']
       