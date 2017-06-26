from django.shortcuts import render
from notification.models import Notification


def notification(request):
    unread_notifications = Notification.objects.filter(recipient=request.profile, status=Notification.NEW).all()
    Notification.objects.filter(recipient=request.profile).update(status=Notification.READ)
    return render(request, 'notifications.html', {'unread_notifications': unread_notifications})