from django.forms import ModelForm
from django.forms.widgets import Select, NumberInput
from django import forms

# Import App Model
from listings.models import Listings
from categories.models import SubCategories, Categories


# Forms
class ListingsForms(ModelForm):

    categories = forms.ModelChoiceField(queryset=Categories.objects.all(),
                                        required=False,
                                        widget=forms.Select(attrs={
                                            'class': 'form-control'}))

    tag = forms.CharField(required=False,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                              'style': 'width: 100%',
                              'data-role': 'tagsinput'}))

    price = forms.DecimalField(label='Cost in Village Hours',
                               widget=forms.NumberInput(attrs={
                                   'class': 'form-control',
                                   'style': 'width: 100%'
                               }))

    class Meta:
        model = Listings
        fields = ['listing_type', 'title', 'description', 'price', 'categories', 'subcategories', 'photo', 'tag']
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
                'class': 'form-control',
            }),
            # 'price': NumberInput(attrs={
            #     'class': 'form-control',
            #     'style': 'width: 100%',
            # }),
            'subcategories': Select(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),

            'tag': forms.TextInput(attrs={'class': 'form-control',
                                          'data-role': 'tagsinput',
                                          'style': 'width: 100%'})
        }
