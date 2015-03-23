# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0004_auto_20150319_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='building_code',
            field=models.CharField(default='', unique=True, max_length=20, verbose_name='Building code'),
            preserve_default=True,
        ),
    ]
