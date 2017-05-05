from django.conf.urls import url, include
from listing_management import urls as listing_management_urls
import listings.views as listing_views

urlpatterns = [
    url(r'^new_listing/', listing_views.add_new_listing, name="new_listing"),
    url(r'^listing_details/([^/]+)/$', listing_views.listing_details, name='listing_details'),
    url(r'^get_listing_info/([^/]+)/$', listing_views.get_listing_info, name='listing_modal_details'),
    url(r'^listing_management/', include(listing_management_urls, namespace='listing_management'))
]