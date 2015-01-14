# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20150107_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='fk_status',
            field=models.ForeignKey(to='ticketing.TicketStatus'),
            preserve_default=True,
        ),
    ]
