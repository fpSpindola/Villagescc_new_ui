import os
import datetime
import pytz
from django.core.files.base import ContentFile
from profile.models import Profile, Settings
from requests import request, HTTPError
from django.core.files.base import ContentFile


def create_profile_data(strategy, user, response, details, is_new=False, *args, **kwargs):
    if is_new:
        if 'fullname' in details:
            full_name = details['fullname']
        else:
            full_name = user.username
        new_profile = Profile(user=user, name=full_name)
        new_profile.user_id = user.id
        new_profile.name = user.username
        new_profile.user.email = details['email'] if 'email' in details else None

        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            img_content = request('GET', url, params={'type': 'large'})
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads',
                                     'facebook', '{0}__social.jpg'.format(user.id))
            with open(file_path, 'wb+') as destination:
                img_file = ContentFile(img_content.content)
                for chunk in img_file.chunks():
                    destination.write(chunk)
            new_profile.photo = 'facebook/{0}__social.jpg'.format(user.id)
            new_profile.save()

            profile_settings = Settings.objects.get(profile_id=new_profile.id)
            profile_settings.email = details['email'] if 'email' in details else None
            profile_settings.feed_radius = -1
            profile_settings.save()
            return
        except Exception as e:
            print(e)
    elif user.date_joined >= (datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(hours=1)):
        existing_profile = Profile.objects.get(user_id=user.id)
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            img_content = request('GET', url, params={'type': 'large'})
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads',
                                     'facebook', '{0}__social.jpg'.format(user.id))
            with open(file_path, 'wb+') as destination:
                img_file = ContentFile(img_content.content)
                for chunk in img_file.chunks():
                    destination.write(chunk)
            existing_profile.photo = 'facebook/{0}__social.jpg'.format(user.id)
            existing_profile.save()
        except Exception as e:
            print(e)