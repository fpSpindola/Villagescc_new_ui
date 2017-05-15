from django.db import models
from profile.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class TagProfile(models.Model):
    tag = models.ManyToManyField(Tag, null=False, blank=False)
    profile_id = models.ForeignKey(Profile, null=True, blank=True, related_name="tag_profile")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
