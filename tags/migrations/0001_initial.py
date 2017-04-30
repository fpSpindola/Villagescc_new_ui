from django.db import models, migrations
from django.conf import settings
import general.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', general.models.VarCharField(max_length=100, verbose_name='Name', blank=False)),
                ('created_at', models.DateTimeField(auto_now_add=True))
            ],
        ),
        migrations.CreateModel(
            name='TagProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(blank=True, on_delete=models.deletion.CASCADE, to='tags.Tag')),
                ('profile', models.ForeignKey(blank=True, on_delete=models.deletion.CASCADE, to='profile.Profile')),

            ],
        ),
        migrations.CreateModel(
            name='TagListing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(blank=True, on_delete=models.deletion.CASCADE, to='tags.Tag')),
                ('listing', models.ForeignKey(blank=True, on_delete=models.deletion.CASCADE, to='listings.Listings')),
            ]
        )
    ]
