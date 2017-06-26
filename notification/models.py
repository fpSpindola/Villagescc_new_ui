from django.db import models
from profile.models import Profile


class Notification(models.Model):
    notifier = models.ForeignKey(Profile, related_name='notifier')
    recipient = models.ForeignKey(Profile, related_name='notification_received')
    notification_type = models.CharField()
    status = models.CharField(choices=('READ', 'NEW'))
    created_at = models.DateTimeField(auto_now_add=True)