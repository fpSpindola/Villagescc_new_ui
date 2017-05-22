from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from listings.models import Listings
from listings.forms import ListingsForms
from tags.models import Tag


def view_listings(request):
    listings = Listings.objects.filter(user_id=request.user.id).all()
    return render(request, 'listing_management/manage_listings.html', {'listings': listings})


def edit_listing(request, listing_id):
    listing_form = ListingsForms()
    listing = Listings.objects.get(id=listing_id, user_id=request.user.id)

    if not request.user.id == listing.user_id:
        messages.add_message(request, messages.ERROR, 'You are not allowed to do this')
        return HttpResponseRedirect(reverse('listing_management:manage_listings'))

    if not listing:
        messages.add_message(request, messages.ERROR, 'No listing has been found with this id')
        return HttpResponseRedirect(reverse('listing_management:manage_listings'))
    if request.method == 'POST':
        form = ListingsForms(request.POST, request.FILES)
        if form.is_valid():
            listing.listing_type = form.cleaned_data['listing_type']
            listing.title = form.cleaned_data['title']
            listing.description = form.cleaned_data['description']
            listing.price = form.cleaned_data['price']
            listing.subcategories = form.cleaned_data['subcategories']
            if form.cleaned_data["photo"]:
                listing.photo = form.cleaned_data['photo']
            elif listing.photo:
                listing.photo = listing.photo
            else:
                listing.photo = ""
            listing.save()

            tags_list = form.cleaned_data['tag'].split(',')
            if tags_list and tags_list[0] == u'':
                tags_to_delete = listing.tag.all()
                if tags_to_delete:
                    for each_tag_delete in tags_to_delete:
                        Tag.objects.filter(id=each_tag_delete.id).delete()
                    messages.add_message(request, messages.SUCCESS, 'Listing edited with success.')
                    return HttpResponseRedirect(reverse('listing_management:manage_listings'))
            else:
                listing.tag.all().delete()
                for tag in tags_list:
                    new_tag = Tag(name=tag)
                    try:
                        new_tag.save()
                        new_tag.listings_set.add(listing)
                    except IntegrityError as e:
                        existing_tag = Tag.objects.get(name=tag)
                        existing_tag.listings_set.add(listing)
                messages.add_message(request, messages.SUCCESS, 'Listing edited with success.')
                return HttpResponseRedirect(reverse('listing_management:manage_listings'))
        else:
            messages.add_message(request, messages.ERROR, 'An error has occurred, please try again later.')
            return render(request, 'listing_management/manage_listings.html', {'form': form, 'listings_form': listing})
    else:
        tags_to_template = ''
        tags = listing.tag.all().values('name')
        if tags:
            for each_tag in tags:
                tags_to_template = tags_to_template + each_tag['name'].encode() + ','
        form = ListingsForms(instance=listing,
                             initial={'listing_type': listing.listing_type,
                                      'title': listing.title,
                                      'description': listing.description,
                                      'price': listing.price,
                                      'subcategories': listing.subcategories,
                                      'tag': tags_to_template})
        return render(request, 'listing_management/edit_listing.html', {'form': form})

    messages.add_message(request, messages.ERROR, form.errors)
    form = ListingsForms(initial={'listing_type': listing.listing_type,
                                  'title': listing.title,
                                  'description': listing.description,
                                  'price': listing.price,
                                  'subcategories': listing.subcategories,
                                  'photo': listing.photo})
    return render(request, 'listing_management/edit_listing.html', {'form': form, 'listings_form': listing})


@transaction.atomic
def delete_listing(request):
    if request.method == 'POST' and request.is_ajax():
        list_listings_to_remove = []
        for listing_id in request.POST.getlist('ids[]'):
            list_listings_to_remove.append(int(listing_id))
        listing_to_remove = Listings.objects.filter(id__in=list_listings_to_remove)
        try:
            for listings in listing_to_remove:
                Listings.objects.filter(id=listings.id).delete()
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'An error occurred, please try again later.')
    return HttpResponseRedirect(reverse('listing_management:manage_listings'))