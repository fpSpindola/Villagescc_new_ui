from datetime import datetime
from django.forms import ModelForm
from django.forms.widgets import Select, NumberInput
from django import forms
from django.utils.translation import ugettext_lazy as _

from listings.models import Listings

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

    d = forms.DateTimeField(
        label="Up to date", required=False, input_formats=[DATE_FORMAT])

    trusted = forms.BooleanField(label='Trusted only', required=False,
                                 widget=forms.CheckboxInput(attrs={
                                     'class': 'form-control checkbox-inline', 'style': 'vertical-align: middle'
                                 }))

    q = forms.CharField(label='Search', required=False,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control'}))

    radius = forms.TypedChoiceField(
        required=False, choices=RADIUS_CHOICES, coerce=int, empty_value=None,
        widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, data, profile, location=None, *args, **kwargs):
        data = data.copy()
        if 'radius' not in data:
            default_radius = (profile and profile.settings.feed_radius or DEFAULT_RADIUS)
            data['radius'] = default_radius
            self._explicit_radius = False
        super(FormListingsSettings, self).__init__(data, *args, **kwargs)

    def get_results(self):
        data = self.cleaned_data
        date = data.get('d') or datetime.now()
        tsearch = data.get('q')
        radius = data['radius']
        query_radius = radius
        if radius == INFINITE_RADIUS:
            query_radius = None
        trusted = data['trusted']
        # while True:
        items, count = Listings.objects.get_items_and_remaining()
            # query_radius = next_query_radius(query_radius)
            # self.data['radius'] = query_radius
            # if query_radius == INFINITE_RADIUS:
            #     query_radius = None
            # continue
        return items, count


def next_query_radius(radius):
    i = RADII.index(radius)
    return RADII[i + 1]