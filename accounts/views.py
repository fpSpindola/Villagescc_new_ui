# Django http and shortcuts import
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# From Contrib
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login as django_login_view
from sign_in.views import SignInUserLogIn

# Django User
from django.contrib.auth.models import User

from profile.models import Profile

# App Forms
from accounts.forms import RegisterForm, UserForm, ProfileCreationForm, ProfileSettingsForm


# Create your views here.
def signup_view(request):
    """
    POST method with email and username and password register new user
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)

            obj, created = Profile.objects.get_or_create(user=user)

            # Successfull login redirect to login page
            return HttpResponseRedirect(reverse('accounts:login'))
        else:
            print form.errors
            # If error found we need to show to the frontend using form errors
            # Returning same form contains context of errors attripute
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        # Get method should return empty Form
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Login view function takes no arguemnt if supplied username and password
    matches then request will authenticate with login and return with User context
    """
    if request.method == 'POST':
        form = UserForm()
        if form.is_valid():
            # Will not throw error because input have value=""
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
            except:
                messages.error(request, "User not found")
                return redirect(SignInUserLogIn, {'form': form})
        else:
            # Password wrong
            messages.error(request, 'Username or Password is wrong')
            return render(request, 'accounts/sign_in.html', {'form': form})
    return render(request, 'accounts/sign_in.html')


def logout_view(request):
    """ Remove user from the request """
    logout(request)
    return HttpResponseRedirect(reverse("frontend:home"))


def profile(request, username=None):
    """
    Profile takes no arugment and returns the listings attripute
    """
    if username:
        profile = Profile.objects.get(user__username=username)
    else:
        profile = Profile.objects.get(user__username=request.user.username)
    return render(request, 'accounts/profile.html', {'profile': profile})


def my_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if profile == request.profile:
        template = 'my_profile.html'
    else:
        template = 'profile.html'
        if request.profile:
            my_endorsement = request.profile.endorsement_for(profile)
            account = profile.account(request.profile)
    return locals(), template


def settings_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_obj = Profile.objects.get(user=request.user)
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # TODO: Getting password from the request Object and save
            password = request.POST['password']
            return HttpResponseRedirect(reverse('accounts:settings'))
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileSettingsForm()
    return render(request, 'accounts/setting.html', {'user_form': user_form, 'profle_form': profile_form})
