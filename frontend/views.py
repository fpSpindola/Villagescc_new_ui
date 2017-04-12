from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.gis.db.models import GeoManager
from django.db.models import Q
# from general.util import render
from django.shortcuts import render
from geo.util import location_required
from feed.forms import FeedFilterForm, DATE_FORMAT
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
# Forms
from listings.forms import ListingsForms
from feed.forms import FeedFilterForm, DATE_FORMAT
from relate.forms import Endorsement, EndorseForm, AcknowledgementForm
# models

from relate.models import Endorsement
from profile.models import Profile
from listings.models import Listings
from categories.models import Categories, SubCategories


def home(request, type_filter=None, item_type=None, template='frontend/home.html', poster=None, recipient=None,
         extra_context=None, do_filter=False):
    """
    This is home page but before logged in user will see this pages
    returns before login home.
    url: /home
    """
    # POST Request
    endorsement = None
    if item_type:
        form = FeedFilterForm(request.GET, request.profile, request.location, item_type,
                              poster, recipient, do_filter)
        trust_form = EndorseForm(instance=endorsement)
        if form.is_valid():
            feed_items, remaining_count = form.get_results()
            if do_filter:
                form.update_sticky_filter_prefs()
        else:
            raise Exception(unicode(form.errors))
        if feed_items:
            next_page_date = feed_items[-1].date
        else:
            next_page_date = None
        url_params = request.GET.copy()
        url_params.pop('d', None)
        url_param_str = url_params.urlencode()
        if next_page_date:
            url_params['d'] = next_page_date.strftime(DATE_FORMAT)
        next_page_param_str = url_params.urlencode()

        categories_list = Categories.objects.all()
        item_sub_categories = SubCategories.objects.all().filter(categories=1)
        services_sub_categories = SubCategories.objects.all().filter(categories=2)
        rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
        housing_sub_categories = SubCategories.objects.all().filter(categories=4)

        context = locals()
        context.update(extra_context or {})
        return render(request, 'frontend/home.html', {'url_params': url_params, 'feed_items': feed_items,
                                                      'next_page_date': next_page_date, 'context': context,
                                                      'form': form, 'poster': poster, 'do_filter': do_filter,
                                                      'remaining_count': remaining_count,
                                                      'item_type': item_type, 'template': template,
                                                      'url_param_str': url_param_str,
                                                      'next_page_param_str': next_page_param_str,
                                                      'extra_context': extra_context,
                                                      'recipient': recipient,
                                                      'item_sub_categories': item_sub_categories,
                                                      'services_sub_categories': services_sub_categories,
                                                      'rideshare_sub_categories': rideshare_sub_categories,
                                                      'housing_sub_categories': housing_sub_categories,
                                                      'categories': categories_list, 'trust_form': trust_form})
    else:
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

        if type_filter == 'trusted':
            trusted_only = request.profile.trusted_profiles.all().order_by('-created')

        if type_filter:
            listings = Listings.objects.all().filter(subcategories__sub_categories_text=type_filter)
        else:
            trust_form = EndorseForm(instance=endorsement, endorser=None, recipient=None)
            payment_form = AcknowledgementForm(max_ripple=None, initial=request.GET)
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
            'categories': categories_list, 'trusted_only': trusted_only,
            'trust_form': trust_form,
            'payment_form': payment_form})
