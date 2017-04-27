# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20170424_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='description',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
