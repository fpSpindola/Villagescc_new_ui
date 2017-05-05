from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from listings.models import Listings
from listings.forms import ListingsForms


def view_listings(request):
    listings = Listings.objects.filter(user_id=request.user.id).all()
    return render(request, 'listing_management/manage_listings.html', {'listings': listings})


def edit_listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id, user_id=request.user.id)

    if not request.user.id == listing.user_id:
        messages.add_message(request, messages.ERROR, 'You are not allowed to do this')
        return HttpResponseRedirect(reverse('listing_management:manage_listings'))

    if not listing:
        messages.add_message(request, messages.ERROR, 'No listing has been found with this id')
        return HttpResponseRedirect(reverse('listing_management:manage_listings'))
    if request.method == 'POST':
        form = ListingsForms(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data['listing_type'] == listing.listing_type and \
                                form.cleaned_data['title'] == listing.title and \
                                form.cleaned_data['description'] == listing.description and \
                                form.cleaned_data['price'] == listing.price and \
                                form.cleaned_data['subcategories'] == listing.subcategories:
                        messages.add_message(request, messages.ERROR, 'No changes were identified')
                else:
                    listing.listing_type = form.cleaned_data['listing_type']
                    listing.title = form.cleaned_data['title']
                    listing.description = form.cleaned_data['description']
                    listing.price = form.cleaned_data['price']
                    listing.subcategories = form.cleaned_data['subcategories']
                    listing.save()
                    messages.add_message(request, messages.SUCCESS, 'Listing edited with success.')
                    HttpResponseRedirect(reverse('listing_management:manage_listings'))
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'An error has occurred, please try again later.')
                return render(request, 'listing_management/manage_listings.html', {'form': form, 'listings': listing})
    else:
        form = ListingsForms(initial={'listing_type': listing.listing_type,
                                      'title': listing.title,
                                      'description': listing.description,
                                      'price': listing.price,
                                      'subcategories': listing.subcategories})
        return render(request, 'listing_management/edit_listing.html', {'form': form})
    HttpResponseRedirect(reverse('listing_management:manage_listings'))


@transaction.atomic
def delete_listing(request):
    if request.method == 'POST' and request.is_ajax():
        listing_to_remove = Listings.objects.filter(id__in=[",".join(request.POST.getlist('ids[]'))])
        try:
            for listings in listing_to_remove:
                Listings.objects.filter(id=listings.id).delete()
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'An error occurred, please try again later.')
    return HttpResponseRedirect(reverse('listing_management:manage_listings'))