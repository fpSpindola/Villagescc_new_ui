import json
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from listings.models import Listings
from django.core.urlresolvers import reverse
from listings.forms import ListingsForms
from .schemas import SubmitListingSchema


def add_new_listing(request):
    schema = SubmitListingSchema()
    data, errors = schema.load(request.POST)
    if not errors:
        form = ListingsForms(request.POST, request.FILES)
        if form.is_valid():
            try:
                listing = form.save(commit=False)
                listing.user_id = request.profile.user_id
                listing.save()
                return HttpResponseRedirect(reverse('frontend:home'))
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse('frontend:home'))
    else:
        return JsonResponse({'errors': errors}, status=400)


def submit_listing_api(request):
    values = json.loads(request.body.decode('UTF-8'))
    schema = SubmitListingSchema()
    data, errors = schema.load(values)
    if not errors:
        listing = ListingsForms()
        listing.title = data['title']
        listing.listing_type = data['listing_type']
        listing.description = data['description']
        listing.price = data['price']
        listing.subcategories = data['subcategories']
        return JsonResponse({'msg': 'Successfully added listing'})
    return JsonResponse({'errors': errors}, status=400)


def listing_details(request, listing_id):
    listing = Listings.objects.filter(id=listing_id)
    if listing:
        messages.add_message(request, messages.SUCCESS, 'Listing overview found!')
        return render(request, 'listing_details.html', {'listing': listing})
    else:
        messages.add_message(request, messages.ERROR, 'An error ocurred when trying to retrieve the listing info')
        return render(request, 'listing_details.html')

