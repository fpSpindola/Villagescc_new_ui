from tags.models import Tag
from django.contrib.auth.models import User
from django.db import models
from categories.models import SubCategories
from django.contrib.gis.db.models import GeoManager

OFFER = 'Offer'
REQUEST = 'Request'
TEACH = 'Teach'
LEARN = 'Learn'
GIFT = 'Gift'

LISTING_TYPE = (
    ('OFFER', OFFER),
    ('REQUEST', REQUEST),
    ('TEACH', TEACH),
    ('LEARN', LEARN),
    ('GIFT', GIFT),
)

TRUSTED_SUBQUERY = (
    "feed_feeditem.poster_id in "
    "(select to_profile_id from profile_profile_trusted_profiles "
    "    where from_profile_id = %s)")

# Create your models here.


class ListingManager(GeoManager):
    def get_feed_and_remaining(self, *args, **kwargs):
        """
        Returns feed and count of remaining items not returned after
        limiting the query.
        """
        count_kwargs = kwargs.copy()
        count_kwargs.pop('limit', None)
        count = self.get_feed_count(*args, **count_kwargs)
        if count > 0:
            items = self.get_feed(*args, **kwargs)
        else:
            items = []
        return items, count - len(items)


class Listings(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    subcategories = models.ForeignKey(SubCategories, null=True, blank=True)
    # tag = models.ForeignKey(TagListing, null=True, blank=True)

    listing_type = models.CharField(max_length=100, choices=LISTING_TYPE)
    photo = models.ImageField(upload_to='listings', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True)

    @property
    def date(self):
        return self.updated