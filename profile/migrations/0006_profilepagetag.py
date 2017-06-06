# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_profile_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePageTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listing_type', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(related_name='profile', to='profile.Profile')),
                ('tag', models.ForeignKey(related_name='profile_tag', blank=True, to='tags.Tag', null=True)),
            ],
        ),
    ]
