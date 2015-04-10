# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0016_auto_20150407_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='postcode',
            field=models.CharField(verbose_name='Postcode', null=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='building',
            name='vicinity',
            field=models.CharField(verbose_name='Vicinity name', default='', max_length=45, blank=True),
        ),
    ]
