from django import forms
from .models import Location


class SearchLocationForm(forms.Form):
    location = forms.CharField(max_length=120, label='Искать')


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'country', 'latitude', 'longitude', 'user')