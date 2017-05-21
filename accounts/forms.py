from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

# App model
from profile.models import Profile

# Forms


class RegisterForm(ModelForm):
    """ Signup form """
    terms_of_service = forms.BooleanField(label='I agree with terms of service', required=True,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Overriding form to set email is required because User email is optional
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserForm(ModelForm):
    """
    User form to update the user information in the settings page
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user']


class ProfileSettingsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
