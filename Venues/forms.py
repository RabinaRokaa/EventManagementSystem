from django import forms
from .models import Venues
from .fields import MultiFileField


class VenuesForm(forms.ModelForm):
    # Venue_image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
    Venue_image= MultiFileField()

    class Meta:
        model = Venues
        fields = ['Name', 'Location', 'Type', 'Description', 'Capacity', 'Cost', 'Venue_image']


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)    
    #     self.fields['Venue_image'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))