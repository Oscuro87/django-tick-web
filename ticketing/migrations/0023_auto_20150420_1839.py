# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0022_auto_20150416_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fk_status',
            field=models.ForeignKey(verbose_name='Status', to='ticketing.TicketStatus'),
        ),
    ]
