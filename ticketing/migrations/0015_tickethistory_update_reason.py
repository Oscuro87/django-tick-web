# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0014_auto_20150113_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickethistory',
            name='update_reason',
            field=models.CharField(default='No reason given.', max_length=200, blank=True, verbose_name='Update reason'),
            preserve_default=True,
        ),
    ]
