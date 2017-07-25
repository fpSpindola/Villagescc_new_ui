import os
import django
import csv

os.environ["DJANGO_SETTINGS_MODULE"] = "ccproject.settings"

django.setup()

from profile.models import Profile
from django.contrib.auth.models import User


profiles = Profile.objects.all()
writer = csv.writer(open("profiles.csv", "ab"), delimiter=',', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['name, email, city, state, neighborhood'])
for each_profile in profiles:
    profile_data = [each_profile.name, each_profile.email, each_profile.location.city, each_profile.location.state,
                    each_profile.location.neighborhood]
    try:
        writer.writerow(profile_data)
    except Exception as e:
        try:
            profile_data = [each_profile.name, each_profile.email]
            writer.writerow(profile_data)
        except Exception as e:
            print(e)



# reader = csv.reader(open("friends.csv", "rb"), delimiter=' ')
