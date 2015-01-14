# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0007_auto_20150110_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickethistory',
            name='fk_ticket',
            field=models.ForeignKey(on_delete='CASCADE', to='ticketing.Ticket'),
            preserve_default=True,
        ),
    ]
