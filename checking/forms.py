from django import forms 


class AvailabilityForm(forms.Form):
    categories = [('Marriage', 'Marriage'),
                  ('Birthday', 'Birthday'),
                  ('Conference', 'Conference'),
                  ('Anniversary', 'Anniversary')]
    
    event_type = forms.ChoiceField(choices=categories, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M',])
    check_out= forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'])
