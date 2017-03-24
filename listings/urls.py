from django.conf.urls import url, include
import listings.views as listing_views

urlpatterns = [
    url(r'^new_posting/', listing_views.add_new_listing, name="new_posting"),
]