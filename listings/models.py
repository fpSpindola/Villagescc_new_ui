from django.conf import settings
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


class ListingsManager(GeoManager):
    def get_items_and_remaining(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        count_kwargs = kwargs.copy()
        count_kwargs.pop('limit', None)
        count = self.get_items_count(self, *args, **count_kwargs)
        if count > 0:
            items = self.get_items(*args, **kwargs)
        else:
            items = []
        return items, count - len(items)

    def get_items_count(self, *args, **kwargs):
        return self._item_query(*args, **kwargs).count()

    def get_items(self, *args, **kwargs):
        limit = kwargs.pop('limit', settings.FEED_ITEMS_PER_PAGE)
        query = self._item_query(*args, **kwargs)[:limit]
        return query

    def _item_query(self, listing=None, location=None, radius=None, tsearch=None, trusted_only=False,
                    up_to_date=None):
        query = self.get_queryset().order_by('-created')
        if up_to_date:
            query = query.filter(created__lt=up_to_date)
        return query


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

    objects = ListingsManager()

    @property
    def date(self):
        return self.updated