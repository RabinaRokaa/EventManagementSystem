from django import forms
from .models import booking





class Meta:
        model = booking
        fields = ['Event_Type', 'Name','' 'Type', 'Description', 'Cost', ]


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)    
    #     self.fields['Venue_image'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))