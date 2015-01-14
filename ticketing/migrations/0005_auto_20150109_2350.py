# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0004_auto_20150109_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fk_building',
            field=models.ForeignKey(to='ticketing.Building'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_category',
            field=models.ForeignKey(to='ticketing.EventCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_channel',
            field=models.ForeignKey(to='ticketing.Channel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_company',
            field=models.ForeignKey(null=True, to='ticketing.Company', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_manager',
            field=models.ForeignKey(related_name='gestionnaire', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_priority',
            field=models.ForeignKey(to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_renter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='locataire'),
            preserve_default=True,
        ),
    ]
