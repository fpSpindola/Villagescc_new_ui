from django.conf.urls import url, include
from categories.subcategories_manager import views as subcategories_views

urlpatterns = [
    url(r'^$', subcategories_views.view_subcategories, name='manage_categories')
]