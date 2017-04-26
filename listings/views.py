from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from listings.models import Listings
from django.core.urlresolvers import reverse
from listings.forms import ListingsForms


def add_new_listing(request):
    if request.method == 'POST':
        if 'initial' in request.POST:
            form = ListingsForms()
        else:
            form = ListingsForms(request.POST, request.FILES)
            if form.is_valid():
                try:
                    listing = form.save(commit=False)
                    listing.user_id = request.profile.user_id
                    listing.save()
                except Exception as e:
                    print(e)
                return HttpResponseRedirect(reverse('frontend:home'))
    else:
        form = ListingsForms()
    return JsonResponse({'data': 'ok'})
    # return render(request, 'frontend/home.html', {'form': form})


def listing_details(request, listing_id):
    listing = Listings.objects.filter(id=listing_id)
    if listing:
        messages.add_message(request, messages.SUCCESS, 'Listing overview found!')
        return render(request, 'listing_details.html', {'listing': listing})
    else:
        messages.add_message(request, messages.ERROR, 'An error ocurred when trying to retrieve the listing info')
        return render(request, 'listing_details.html')

