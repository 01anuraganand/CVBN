from django import forms
from django.forms import fields
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['photo']
        # widgets = {
        #     'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'file'
        })

