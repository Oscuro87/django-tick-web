# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_company',
            field=models.OneToOneField(blank=True, default=None, null=True, to='ticketing.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_parent_category',
            field=models.OneToOneField(blank=True, default=None, null=True, to='ticketing.EventCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_priority',
            field=models.ForeignKey(to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
    ]
