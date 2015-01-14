# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0008_auto_20150110_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fk_manager',
            field=models.ForeignKey(related_name='manager', blank=True, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_renter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
