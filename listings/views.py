from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from listings.models import Listings
from django.core.urlresolvers import reverse
from listings.forms import ListingsForms


def add_new_listing(request):
    if request.method == 'POST':
        if 'initial' in request.POST:
            form = ListingsForms()
        else:
            form = ListingsForms(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('frontend:home'))
    else:
        form = ListingsForms()
    return render(request, 'frontend/home.html', {'form': form})