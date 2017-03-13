from django.contrib import messages
from django.shortcuts import render, redirect
from pages.forms import AnonymousFeedbackForm, UserFeedbackForm
from django.utils.translation import ugettext_lazy as _

MESSAGES = {
    'feedback_sent': _("Thank you for your feedback."),
}

def how_it_works(request):
    return render(request, 'how_it_works.html')


def motivation(request):
    return render(request, 'motivation.html')


def privacy(request):
    return render(request, 'privacy.html')


def developers(request):
    return render(request, 'developers.html')


def donate(request):
    return render(request, 'donate.html')


def contact_us(request):
    if request.method == 'POST':
        if request.profile:
            form = UserFeedbackForm(request.profile, request.POST)
        else:
            form = AnonymousFeedbackForm(request.POST)
        if form.is_valid():
            form.send()
            messages.info(request, MESSAGES['feedback_sent'])
            return redirect('home')
    else:
        if request.profile:
            form = UserFeedbackForm(request.profile)
        else:
            form = AnonymousFeedbackForm()
    return render(request, 'feedback.html', {'form': form})