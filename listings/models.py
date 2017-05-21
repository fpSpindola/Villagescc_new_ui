from django.conf import settings
from tags.models import Tag
from django.contrib.auth.models import User
from django.db import models
from categories.models import SubCategories
from django.contrib.gis.db.models import GeoManager, Q

OFFER = 'OFFER'
REQUEST = 'REQUEST'
TEACH = 'TEACH'
LEARN = 'LEARN'
# GIFT = 'GIFT'

LISTING_TYPE = (
    ('OFFER', OFFER),
    ('REQUEST', REQUEST),
    ('TEACH', TEACH),
    ('LEARN', LEARN),
    # ('GIFT', GIFT),
)

LISTING_TYPE_CHECK = ['OFFER', 'REQUEST', 'TEACH', 'LEARN']

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
        items = []
        for listing_item in query:
            items.append(listing_item)
        return items

    def _item_query(self, profile=None, location=None, radius=None, tsearch=None, trusted_only=False,
                    up_to_date=None, request_profile=None, type_filter=None):
        query = self.get_queryset().order_by('-updated')
        if up_to_date:
            query = query.filter(updated__lt=up_to_date)
        if trusted_only:
            query.extra(select={
                "trusted_listings": "select listings_listings.id from listings_listings "
                                    "inner join profile_profile on (listings_listings.user_id = profile_profile.user_id) "
                                    "where profile_profile.id in "
                                    "(select profile_profile_trusted_profiles.to_profile_id "
                                    "from profile_profile_trusted_profiles "
                                    "where profile_profile_trusted_profiles.from_profile_id = {0} LIMIT 1)".format(request_profile.id)})
        if location and radius:
            query = query.filter(
                Q(user__profile__location__point__dwithin=(location.point, radius)) |
                Q(user__profile__location__isnull=True))

        if tsearch:
            query = query.filter(Q(title__icontains=tsearch) |
                                 Q(description__icontains=tsearch))

        if type_filter:
            if type_filter in LISTING_TYPE_CHECK:
                    query = query.filter(listing_type=type_filter).order_by('-updated')
            else:
                query = query.filter(subcategories__id=type_filter).order_by('-updated')
        return query


class Listings(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=5000, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    subcategories = models.ForeignKey(SubCategories, null=True, blank=True)
    # tag = models.ForeignKey(TagListing, null=True, blank=True)

    listing_type = models.CharField(max_length=100, choices=LISTING_TYPE)
    photo = models.ImageField(upload_to='listings', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tag = models.ManyToManyField(Tag)

    objects = ListingsManager()

    @property
    def date(self):
        return self.updated