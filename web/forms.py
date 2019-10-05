from django import forms
from .models import *

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        exclude = ['checked']
