# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0021_auto_20150416_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country'),
        ),
    ]
