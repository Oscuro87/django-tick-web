# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0014_auto_20150407_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='building_code',
            field=models.CharField(max_length=10, unique=True, default='', verbose_name='Building code', blank=True),
        ),
    ]
