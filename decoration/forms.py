from django import forms
from .models import decoration
from .fields import MultiFileField


class DecorationForm(forms.ModelForm):
    # Venue_image = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
    Decoration_image= MultiFileField()

    class Meta:
        model = decoration
        fields = ['Name', 'Type', 'Description', 'Cost', 'Decoration_image']


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)    
    #     self.fields['Venue_image'] = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))