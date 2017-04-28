from django.conf.urls import url, include
import listings.views as listing_views

urlpatterns = [
    url(r'^new_listing/', listing_views.add_new_listing, name="new_listing"),
    url(r'^listing_details/([^/]+)/$', listing_views.listing_details, name='listing_details'),
]