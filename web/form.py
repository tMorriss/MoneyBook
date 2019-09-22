from django import forms
from .models import *

class DataForm(forms.Form):
    class Meta:
        model = Data
        fields = '__all__'
