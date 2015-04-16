# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0019_auto_20150413_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='city',
            field=models.CharField(blank=True, default='', verbose_name='City name', max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='building_code',
            field=models.CharField(unique=True, blank=True, verbose_name='Building code', max_length=20, default=''),
        ),
    ]
