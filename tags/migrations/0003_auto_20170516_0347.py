# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20170515_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagprofile',
            name='profile_id',
        ),
        migrations.RemoveField(
            model_name='tagprofile',
            name=b'tag',
        ),
        migrations.DeleteModel(
            name='TagProfile',
        ),
    ]
