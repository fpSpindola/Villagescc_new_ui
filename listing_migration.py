import os

os.environ["DJANGO_SETTINGS_MODULE"] = "ccproject.settings"

import django

django.setup()

from post.models import Post
from listings.models import Listings

all_posts = Post.objects.all()
for post in all_posts:
    post_user_id = post.user_id
    post_date = post.date
    if len(post.title) < 220:
        post_title = post.title
    else:
        post_title = post.title[:70]

    post_text = post.text
    post_image = post.image
    post_listing_type = 'REQUEST'

    listing = Listings(title=post_title, listing_type=post_listing_type, photo=post_image, user_id=post_user_id,
                       subcategories_id=2, description=post_title, created=post_date, updated=post_date)
    listing.save()
    print('Listing saved')
