from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Forms
from listings.forms import ListingsForms
from feed.forms import FeedFilterForm, DATE_FORMAT

# models
from listings.models import Listings
from categories.models import Categories, SubCategories


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

    # GET Request
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
    return render(request, 'frontend/home.html',{
        'item_sub_categories': item_sub_categories,
        'services_sub_categories': services_sub_categories,
        'rideshare_sub_categories': rideshare_sub_categories,
        'housing_sub_categories': housing_sub_categories,
        'listings': listings,
        'form': form,
        'categories': categories_list})
