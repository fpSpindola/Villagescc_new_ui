"""ccproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

# all apps urls import
from accounts import urls as accounts_urls
from frontend import urls as frontend_urls
from about import urls as about_urls
from payment_raja import urls as payment_urls
from feed import urls as feed_urls
from geo import urls as geo_urls
from profile import urls as profile_urls
from post import urls as post_urls
from endorsement import urls as endorsement_urls
from relate import urls as relate_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(frontend_urls, namespace='frontend')),
    url(r'^accounts/', include(accounts_urls, namespace='accounts')),
    url(r'^about/', include(about_urls), name='about'),
    url(r'^feed/', include(feed_urls), name='feed'),
    url(r'^profile/', include(profile_urls), name='profile'),
    url(r'^posts/', include(post_urls), name='posts'),
    url(r'^edorsements/', include(endorsement_urls), name='endorsements'),
    url('^relate/', include(relate_urls), name='relate'),
    url(r'', include(geo_urls)),
    url(r'^payment_raja/', include(payment_urls, namespace='payment_raja'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
