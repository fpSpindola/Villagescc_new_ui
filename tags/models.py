from django.db import models, connection, transaction
from general.models import VarCharField, EmailField
from profile.models import Profile
from listings.models import Listings


class Tag(models.Model):
    name = VarCharField()
    created_at = models.DateTimeField(auto_now_add=True)


class TagProfile(models.Model):
    tag_id = models.ForeignKey(Tag, null=False, blank=False)
    profile_id = models.ForeignKey(Profile, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class TagListing(models.Model):
    tag_id = models.ForeignKey(Tag, null=False, blank=False)
    listing_id = models.ForeignKey(Listings, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
