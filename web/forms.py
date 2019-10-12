from django import forms
from .models import *

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        exclude = []

class IntraMoveForm(forms.Form):
    year = forms.IntegerField()
    month = forms.IntegerField()
    day = forms.IntegerField()
    item = forms.CharField(max_length=100, required=False)
    price = forms.IntegerField()
    before_method = forms.IntegerField()
    after_method = forms.IntegerField()