# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='job',
            field=models.TextField(null=True, blank=True),
        ),
    ]
