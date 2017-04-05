from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Forms
from listings.forms import ListingsForms
from feed.forms import FeedFilterForm, DATE_FORMAT

# models
from profile.models import Profile
from listings.models import Listings
from categories.models import Categories, SubCategories

TRUSTED_SUBQUERY = (
    "feed_feeditem.poster_id in "
    "(select to_profile_id from profile_profile_trusted_profiles "
    "    where from_profile_id = %s)")


# Create your views here.
def home(request, type_filter):
    """
    This is home page but before logged in user will see this pages
    returns before login home.
    url: /home
    """
    # POST Request
    if request.method == 'POST':
        form = ListingsForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('frontend:home'))
        else:
            print(form.errors)

    people = None
    trusted_only = None
    # GET Request
    if type_filter == 'people':
        people = Profile.objects.all().order_by('-created')[:100]

    if type_filter == 'trusted_only':
        trusted_only = request.profile.trusted_profiles


    if type_filter:
        listings = Listings.objects.all().filter(subcategories__sub_categories_text=type_filter)
    else:
        listings = Listings.objects.all()
    form = ListingsForms()
    categories_list = Categories.objects.all()
    item_sub_categories = SubCategories.objects.all().filter(categories=1)
    services_sub_categories = SubCategories.objects.all().filter(categories=2)
    rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
    housing_sub_categories = SubCategories.objects.all().filter(categories=4)
    return render(request, 'frontend/home.html', {
        'item_sub_categories': item_sub_categories,
        'services_sub_categories': services_sub_categories,
        'rideshare_sub_categories': rideshare_sub_categories,
        'housing_sub_categories': housing_sub_categories,
        'listings': listings, 'people': people, 'form': form,
        'categories': categories_list, 'trusted_only': trusted_only})
