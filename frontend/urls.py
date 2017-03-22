from django.conf.urls import url

# frontend views import
from frontend import views as frontend_views
from accounts import views as accounts_views


urlpatterns = [
    url(r'^$(?:/(?P<type_filter>[a-zA-Z]+)/)?', frontend_views.home, name='home'),
    url(r'^/home(?:/(?P<type_filter>[a-zA-Z]+)/)?', frontend_views.home, name='home'),
    url(r'^profile/(?P<username>\w+)/$', accounts_views.profile),

]
