from django.conf.urls import url
from about import views as about_views

urlpatterns = [
    url(r'^how_it_works/', about_views.how_it_works, name='how_it_works'),
]