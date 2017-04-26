from django.conf.urls import url

from frontend import views as frontend_views
from accounts import views as accounts_views
from profile.models import Profile


urlpatterns = [
    url(r'^$(?:/(?P<type_filter>[a-zA-Z]+)/)?', frontend_views.home, name='home'),
    url(r'^home/people/(?:/(?P<type_filter>[a-zA-Z]+)/)?', frontend_views.home,
        dict(item_type=Profile, template='profiles.html', do_filter=True), name='home_people'),
    url(r'^home(?:/(?P<type_filter>[a-zA-Z]+)/)?', frontend_views.home, name='home'),
    url(r'^listing/([^/]+)/$', frontend_views.listing_type_filter, name='listing_type'),
    url(r'^categories/(?:(?P<category_type>[a-zA-Z]+)/)?', frontend_views.categories_filter, name='category_type'),
    url(r'^profile/(?P<username>\w+)/$', accounts_views.profile),

]
