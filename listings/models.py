from django.contrib.auth.models import User
from django.db import models
from categories.models import SubCategories

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
# Create your models here.


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
