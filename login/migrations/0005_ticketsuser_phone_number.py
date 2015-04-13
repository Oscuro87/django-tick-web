# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20150407_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsuser',
            name='phone_number',
            field=models.CharField(null=True, max_length=64, verbose_name='User phone number', blank=True),
        ),
    ]
