from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render
from accounts.forms import UserForm
from profile.forms import RegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


class SignInUserLogIn(View):
    form_class = UserForm

    def get(self, request):
        form = self.form_class()
        form.fields.pop('first_name')
        form.fields.pop('last_name')
        form.fields.pop('email')
        return render(request, 'accounts/sign_in.html', {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        # Check the user in database or return
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user:
                # Password matching and user found with authenticate
                login(request, user)
                return HttpResponseRedirect(reverse('frontend:home'))
            else:
                # Password wrong
                messages.error(request, 'Username or Password is wrong')
        except:
            messages.error(request, "User not found")
            return HttpResponseRedirect(reverse('accounts:login'))


class SignInUserRegister(View):
    form_class = RegistrationForm

    def get(self, request):
        form = self.form_class(None)
        # form.fields.pop('new_password')
        return render(request, 'accounts/sign_in.html', {'form': form})

    def post(self, request):
        register = {}
        form = self.form_class(request.POST)
        form.fields.pop('new_password')
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            if repeat_password == password:
                user = User.objects.create_user(username, email=email, password=password)
                if user is not None:
                    login(request, user)
                    register = {'error': 'none'}
            else:
                register = {'error': 'Password Conflict'}
        else:
            register = {'error': 'Username already exists!'}
            for key in form.errors:
                if key == 'email':
                    register = {'error': 'Enter a valid email!'}
        if register['error'] == 'none':
            return render(request, 'home.html', {'form': form,
                                                 'alert_success': {'success': ' Success! ',
                                                                   'message': " You've register with success "}})
        return render(request, 'sign_in.html', {'form': form,
                                                'alert_failed': {'warning': ' Warning!  ',
                                                                 'message': register['error']}})

