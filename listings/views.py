import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from listings.models import Listings
from django.core.urlresolvers import reverse
from listings.forms import ListingsForms
from profile.forms import ContactForm
from relate.forms import AcknowledgementForm
from relate.forms import EndorseForm
from .schemas import SubmitListingSchema
from django.core.exceptions import ObjectDoesNotExist


def add_new_listing(request):
    if request.method == 'POST':
        schema = SubmitListingSchema()
        data, errors = schema.load(request.POST)
        if not errors:
            form = ListingsForms(request.POST, request.FILES)
            if form.is_valid():
                try:
                    listing = form.save(commit=False)
                    listing.user_id = request.profile.user_id
                    listing.save()
                    return JsonResponse({'msg': 'Success!'})
                except Exception as e:
                    print(e)
                    return HttpResponseRedirect(reverse('frontend:home'))
        else:
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = ListingsForms()
    return render(request, 'frontend/home.html', {'form': form})


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
    endorsement = None
    listing_form = ListingsForms()
    try:
        listing = Listings.objects.get(id=listing_id)
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, 'An error ocurred when trying to retrieve the listing info')
        return render(request, 'listing_details.html', {'form': listing_form})
    trust_form = EndorseForm(instance=endorsement, endorser=None, recipient=None)
    payment_form = AcknowledgementForm(max_ripple=None, initial=request.GET)
    contact_form = ContactForm()
    if listing:
        return render(request, 'listing_details.html', {'listing': listing,
                                                        'trust_form': trust_form,
                                                        'payment_form': payment_form,
                                                        'contact_form': contact_form,
                                                        'listing_form': listing_form})


def get_listing_info(request, listing_id):
    data = {}
    try:
        listing = get_object_or_404(Listings, id=listing_id)
        data["listing_title"] = listing.title
        data["listing_price"] = listing.price
        data["listing_photo"] = listing.photo.name
        data["profile_name"] = listing.user.profile.name
        data["profile_location"] = listing.user.profile.location.full_name()
        data["created_at"] = listing.created.date()
        data["stat"] = "ok"
    except Exception as e:
        data["stat"] = "error"
        data["error"] = e
    return JsonResponse({'data': data})

