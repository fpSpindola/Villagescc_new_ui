from django.conf.urls import url, include
import notification.views as notification_views

urlpatterns = [
    url(r'^in_construction/', notification_views.notification_soon, name="notification_soon"),
]