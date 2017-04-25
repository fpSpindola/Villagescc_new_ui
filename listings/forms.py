from django.forms import ModelForm
from django.forms.widgets import Select, NumberInput
from django import forms

# Import App Model
from listings.models import Listings


# Forms
class ListingsForms(ModelForm):
    class Meta:
        model = Listings
        fields = ['listing_type', 'title', 'price', 'subcategories', 'photo']
        widgets = {
            'listing_type': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
            }),
            'description': forms.Textarea(attrs={
                'style': 'width: 570px;'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
            }),
            'subcategories': Select(attrs={
                'class': 'form-control'
            }),
        }
