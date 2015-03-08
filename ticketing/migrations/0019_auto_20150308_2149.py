# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketing', '0018_auto_20150302_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketcomment',
            name='comment',
            field=models.TextField(verbose_name='Comment', default='No comment provided.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketcomment',
            name='date_created',
            field=models.DateTimeField(verbose_name='Comment date', null=True, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketcomment',
            name='fk_commenter',
            field=models.ForeignKey(verbose_name='Commenter', to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketcomment',
            name='fk_ticket',
            field=models.ForeignKey(verbose_name='Ticket', to='ticketing.Ticket', default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='fk_event_category',
            field=models.ForeignKey(null=True, to='ticketing.EventCategory', blank=True, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_status',
            field=models.ForeignKey(verbose_name='Status', to='ticketing.TicketStatus', default=1),
            preserve_default=True,
        ),
    ]
