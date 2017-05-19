from django.forms import ModelForm
from django.forms.widgets import Select, NumberInput
from django import forms
from django.utils.translation import ugettext_lazy as _


INFINITE_RADIUS = -1

RADIUS_CHOICES = (
    (1000, _('Within 1 km')),
    (5000, _('Within 5 km')),
    (10000, _('Within 10 km')),
    (50000, _('Within 50 km')),
    (INFINITE_RADIUS, _('Anywhere')),
)

RADII = [rc[0] for rc in RADIUS_CHOICES]
DEFAULT_RADIUS = 5000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class FormListingsSettings(forms.Form):

    trusted = forms.BooleanField(label='Trusted only', required=False,
                                 widget=forms.CheckboxInput(attrs={
                                     'class': 'form-control checkbox-inline',
                                     'style': 'vertical-align: middle; width: 15px;'
                                 }))

    q = forms.CharField(label='Search', required=False,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Search posts...'}))

    radius = forms.TypedChoiceField(
        required=False, choices=RADIUS_CHOICES, coerce=int, empty_value=None,
        widget=forms.Select(attrs={'class': 'form-control'}))
