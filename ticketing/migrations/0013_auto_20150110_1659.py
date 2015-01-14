# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0012_auto_20150110_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_company',
            field=models.ForeignKey(to='ticketing.Company', default=None, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_building',
            field=models.ForeignKey(to='ticketing.Building', verbose_name='Building'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_category',
            field=models.ForeignKey(to='ticketing.EventCategory', verbose_name='Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_channel',
            field=models.ForeignKey(to='ticketing.Channel', verbose_name='Channel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_company',
            field=models.ForeignKey(to='ticketing.Company', null=True, verbose_name='Company', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_manager',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='gestionnaire', null=True, verbose_name='Manager', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_priority',
            field=models.ForeignKey(to='ticketing.TicketPriority', verbose_name='Priority'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_renter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='locataire', verbose_name='Renter'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_status',
            field=models.ForeignKey(to='ticketing.TicketStatus', verbose_name='Status'),
            preserve_default=True,
        ),
    ]
