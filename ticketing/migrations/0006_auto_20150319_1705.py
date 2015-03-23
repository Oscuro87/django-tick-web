# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0005_auto_20150319_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='building_code',
            field=models.CharField(verbose_name='Building code', unique=True, max_length=6, default=''),
            preserve_default=True,
        ),
    ]
