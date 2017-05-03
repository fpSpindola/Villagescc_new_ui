from django.conf.urls import url, include
from categories.categories_manager import views as categories_views
from categories.subcategories_manager import views as subcategories_views

urlpatterns = [
    url(r'^$', categories_views.view_categories, name='manage_categories')
]