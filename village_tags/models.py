# from listings.models import Listings
from django.db import models
from profile.models import Profile

# from profile.models import Profile

class TagName(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class TagProfile(models.Model):
    tag = models.ManyToManyField(TagName, null=False, blank=False)
    profile_id = models.ForeignKey(Profile, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class TagListing(models.Model):
#     tag = models.ManyToManyField(TagName, null=False, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
