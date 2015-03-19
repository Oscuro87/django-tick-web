# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_auto_20150319_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, default=1),
            preserve_default=False,
        ),
    ]
