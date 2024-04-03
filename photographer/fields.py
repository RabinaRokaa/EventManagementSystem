from django import forms
from django.forms.widgets import ClearableFileInput
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

class MultiFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs, renderer)

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        if data in self.empty_values:
            return []
        elif isinstance(data, UploadedFile):
            return [data]
        elif not hasattr(data, '__iter__'):
            raise ValidationError(self.error_messages['invalid'])
        return data

    def validate(self, value):
        super().validate(value)
        max_size = 5 * 1024 * 1024  # 5MB
        max_files = 5

        for file in value:
            if isinstance(file, UploadedFile) and file.size > max_size:
                raise ValidationError("Too large files");