# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0010_auto_20150110_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_code',
            field=models.CharField(max_length=10, unique=True, verbose_name='Ticket code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickethistory',
            name='fk_manager',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Who changed the status'),
            preserve_default=True,
        ),
    ]
