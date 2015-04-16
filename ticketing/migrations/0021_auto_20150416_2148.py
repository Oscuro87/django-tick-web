# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0020_auto_20150416_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(max_length=60, default='', verbose_name='City name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='vicinity',
            field=models.CharField(blank=True, default='', null=True, verbose_name='Vicinity name', max_length=45),
        ),
    ]
