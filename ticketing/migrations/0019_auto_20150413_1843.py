# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0018_auto_20150408_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_parent_category',
            field=models.ForeignKey(verbose_name='Parent category', null=True, default=None, to='ticketing.EventCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_priority',
            field=models.ForeignKey(to='ticketing.TicketPriority', verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='place',
            name='fk_building',
            field=models.ForeignKey(to='ticketing.Building', verbose_name='Building'),
        ),
        migrations.AlterField(
            model_name='place',
            name='fk_owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
