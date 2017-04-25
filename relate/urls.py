from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from feed.views import feed
from relate.models import Endorsement
from ripple.api import RipplePayment

urlpatterns = patterns(
    'relate.views',
    url(r'^endorse/([^/]+)/$', 'endorse_user', name='endorse_user'),
    url(r'^trust_ajax/([^/]+)/$', 'trust_ajax', name='trust_user_ajax'),
    url(r'^get_listing_info/([^/]+)/$', 'get_listing_info', name='listing_details'),
    url(r'^endorsements/$', login_required(feed),
        dict(item_type=Endorsement, template='endorsements.html',
             do_filter=True),
        name='endorsements'),
    url(r'^endorsements/(\d+)/$', 'endorsement', name='endorsement'),
    url(r'^relationships/$', 'relationships', name='relationships'),
    url(r'^relationships/([^/]+)/$', 'relationship', name='relationship'),
    url(r'^acknowledge/([^/]+)/$', 'acknowledge_user', name='acknowledge_user'),
    url(r'^pay/([^/]+)/$', 'pay_user_ajax', name='pay_user'),
    url(r'^acknowledge_ajax/([^/]+)/$', 'acknowledge_user_ajax', name='acknowledge_user_ajax'),
    url(r'^acknowledgements/$', login_required(feed),
        dict(item_type=RipplePayment, template='acknowledgements.html',
             do_filter=True),
        name='acknowledgements'),
    url(r'^acknowledgements/(\d+)/$', 'view_acknowledgement',
        name='view_acknowledgement'),
)
