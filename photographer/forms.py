from django import forms
from .models import photographer
from .fields import MultiFileField


class PhotographerForm(forms.ModelForm):
    # Venue_image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
    Photographer_image= MultiFileField()

    class Meta:
        model = photographer
        fields = ['Username', 'Phone_Number', 'Email', 'Description', 'Event_type','Cost','Photographer_image']


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)    
    #     self.fields['Venue_image'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))