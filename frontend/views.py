import ripple.api as ripple
# from general.util import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
# Forms
from listings.forms import ListingsForms
from listings.models import LISTING_TYPE_CHECK
from feed.forms import FeedFilterForm, DATE_FORMAT
from notification.models import Notification
from relate.forms import Endorsement, EndorseForm, AcknowledgementForm
from profile.forms import ContactForm
from frontend.forms import FormListingsSettings
from django_user_agents.utils import get_user_agent
# models

from listings.models import Listings
from categories.models import Categories, SubCategories

TRUSTED_SUBQUERY = (
    "feed_feeditem.poster_id in "
    "(select to_profile_id from profile_profile_trusted_profiles "
    "    where from_profile_id = %s)")

LISTINGS_TRUSTED_QUERY = (
    """"select listings_listings.id from listings_listings inner join profile_profile on (listings_listings.user_id = profile_profile.user_id) where profile_profile.id in (select profile_profile_trusted_profiles.to_profile_id from profile_profile_trusted_profiles where profile_profile_trusted_profiles.from_profile_id = {0})""")

SUBQUERY = (
    "profile_profile.id in "
    "(select profile_profile_trusted_profiles.to_profile_id from profile_profile_trusted_profiles "
    "where profile_profile_trusted_profiles.from_profile_id = %s)")


def listing_type_filter(request, listing_type):
    """
    :param request:
    :param category_type:
    :return:
    """
    listing_type_objects = Listings.objects.all().filter(listing_type=listing_type).order_by('-created')
    form = ListingsForms()
    form_listing_settings = FormListingsSettings(initial=request.GET)
    categories_list = Categories.objects.all()
    item_sub_categories = SubCategories.objects.all().filter(categories=1)
    services_sub_categories = SubCategories.objects.all().filter(categories=2)
    rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
    housing_sub_categories = SubCategories.objects.all().filter(categories=4)
    return render(request, 'frontend/home.html', {'listing_form': form, 'listings': listing_type_objects,
                                                  'item_sub_categories': item_sub_categories,
                                                  'services_sub_categories': services_sub_categories,
                                                  'rideshare_sub_categories': rideshare_sub_categories,
                                                  'housing_sub_categories': housing_sub_categories,
                                                  'categories': categories_list, 'listing_type_filter': listing_type,
                                                  'form_listing_settings': form_listing_settings, 'is_listing': True})


def categories_filter(request, category_type):
    """
    :param request:
    :param category_type:
    :return:
    """
    listing_type_objects = Listings.objects.all().filter(subcategories__categories__categories_text=category_type).order_by('-created')
    form = ListingsForms()
    form_listing_settings = FormListingsSettings(initial=request.GET)
    categories_list = Categories.objects.all()
    item_sub_categories = SubCategories.objects.all().filter(categories=1)
    services_sub_categories = SubCategories.objects.all().filter(categories=2)
    rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
    housing_sub_categories = SubCategories.objects.all().filter(categories=4)
    return render(request, 'frontend/home.html', {'listing_form': form, 'listings': listing_type_objects,
                                                  'item_sub_categories': item_sub_categories,
                                                  'services_sub_categories': services_sub_categories,
                                                  'rideshare_sub_categories': rideshare_sub_categories,
                                                  'housing_sub_categories': housing_sub_categories,
                                                  'categories': categories_list, 'subcategory_name': category_type,
                                                  'form_listing_settings': form_listing_settings,
                                                  'category_filter': category_type, 'is_listing': True})


def get_listings_and_remaining(listings):
    count = len(listings)
    if count > 0:
        limit = settings.LISTINGS_PER_PAGE
        query = listings[:limit]
        return query, count - len(query)


def home(request, type_filter=None, item_type=None, template='frontend/home.html', poster=None, recipient=None,
         extra_context=None, do_filter=False):
    """

    url: /home
    """
    # max_amount = ripple.max_payment(request.profile, recipient)

    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        user_agent_type = 'mobile'
    else:
        user_agent_type = 'desktop'
    endorsement = None
    if item_type:
        form = FeedFilterForm(request.GET, request.profile, request.location, item_type,
                              poster, recipient, do_filter)
        trust_form = EndorseForm(instance=endorsement, endorser=None, recipient=None)
        if form.is_valid():
            feed_items, remaining_count = form.get_results(form.data.get('radio-low'),
                                                           form.data.get('radio-high'),
                                                           form.data.get('referral-radio'))
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

        listing_form = ListingsForms()
        categories_list = Categories.objects.all()
        item_sub_categories = SubCategories.objects.all().filter(categories=1)
        services_sub_categories = SubCategories.objects.all().filter(categories=2)
        rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
        housing_sub_categories = SubCategories.objects.all().filter(categories=4)
        trust_form = EndorseForm(instance=endorsement, endorser=None, recipient=None)
        payment_form = AcknowledgementForm(max_ripple=None, initial=request.GET)
        contact_form = ContactForm()
        notification_number = Notification.objects.filter(status='NEW', recipient=request.profile).count()

        context = locals()
        context.update(extra_context or {})
        return render(request, 'frontend/home.html',
                      {'url_params': url_params, 'feed_items': feed_items,
                       'next_page_date': next_page_date, 'context': context,
                       'form': form, 'listing_form': listing_form,
                       'poster': poster, 'do_filter': do_filter,
                       'remaining_count': remaining_count,
                       'item_type': item_type, 'template': template,
                       'url_param_str': url_param_str,
                       'next_page_param_str': next_page_param_str,
                       'extra_context': extra_context,
                       'recipient': recipient, 'user_agent_type': user_agent_type,
                       'item_sub_categories': item_sub_categories,
                       'services_sub_categories': services_sub_categories,
                       'rideshare_sub_categories': rideshare_sub_categories,
                       'housing_sub_categories': housing_sub_categories,
                       'categories': categories_list, 'trust_form': trust_form,
                       'payment_form': payment_form, 'contact_form': contact_form,
                       'notification_number': notification_number})
    else:
        if request.method == 'POST':
            form = ListingsForms(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('frontend:home'))
            else:
                print(form.errors)

        subcategory_name = None
        people = None
        trusted_only = None
        # GET Request
        form_listing_settings = FormListingsSettings(request.GET, request.profile, request.location, type_filter,
                                                     do_filter)
        if form_listing_settings.is_valid():
            listing_items, remaining_count = form_listing_settings.get_results()

        if listing_items:
            next_page_date = listing_items[-1].date
        else:
            next_page_date = None
        url_params = request.GET.copy()
        url_params.pop('d', None)
        url_param_str = url_params.urlencode()
        if next_page_date:
            url_params['d'] = next_page_date.strftime(DATE_FORMAT)
        next_page_param_str = url_params.urlencode()

        trust_form = EndorseForm(instance=endorsement, endorser=None, recipient=None)
        payment_form = AcknowledgementForm(max_ripple=None, initial=request.GET)
        contact_form = ContactForm()

        form = ListingsForms()
        profile = recipient
        categories_list = Categories.objects.all()
        subcategories = SubCategories.objects.all()
        if type_filter in LISTING_TYPE_CHECK:
            # is listing_type filter
            item_type_name = type_filter
        else:
            try:
                SubCategories.objects.filter(id=type_filter)
                # is subcategory id
                item_type_name = SubCategories.objects.filter(id=type_filter).values('sub_categories_text')[0]['sub_categories_text']
            except:
                # is category filter
                item_type_name = type_filter

        item_sub_categories = SubCategories.objects.all().filter(categories=1)
        services_sub_categories = SubCategories.objects.all().filter(categories=2)
        rideshare_sub_categories = SubCategories.objects.all().filter(categories=3)
        housing_sub_categories = SubCategories.objects.all().filter(categories=4)

        notification_number = Notification.objects.filter(status='NEW', recipient=request.profile).count()

        return render(request, 'frontend/home.html', {
            'item_sub_categories': item_sub_categories, 'subcategories': subcategories,
            'services_sub_categories': services_sub_categories, 'rideshare_sub_categories': rideshare_sub_categories,
            'housing_sub_categories': housing_sub_categories, 'user_agent_type': user_agent_type,
            'people': people, 'listing_form': form, 'categories': categories_list,
            'trusted_only': trusted_only, 'trust_form': trust_form, 'payment_form': payment_form,
            'contact_form': contact_form, 'form_listing_settings': form_listing_settings,
            'item_type_name': item_type_name, 'is_listing': True, 'url_params': url_params,
            'listing_items': listing_items, 'next_page_date': next_page_date, 'remaining_count': remaining_count,
            'next_page_param_str': next_page_param_str, 'listing_type_filter': type_filter,
            'notification_number': notification_number})


def pre_home(request):
    return render(request, 'home_banner.html')