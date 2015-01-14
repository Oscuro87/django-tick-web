# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0005_auto_20150109_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickethistory',
            name='fk_manager',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='Who changed the status'),
            preserve_default=True,
        ),
    ]
