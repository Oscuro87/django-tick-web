# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0017_auto_20150408_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image_folder_name',
            field=models.CharField(null=True, blank=True, max_length=128, verbose_name="Name of this ticket's images folder"),
        ),
        migrations.AlterField(
            model_name='building',
            name='postcode',
            field=models.CharField(null=True, blank=True, max_length=10, default='', verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='building',
            name='vicinity',
            field=models.CharField(null=True, blank=True, max_length=45, default='', verbose_name='Vicinity name'),
        ),
    ]
