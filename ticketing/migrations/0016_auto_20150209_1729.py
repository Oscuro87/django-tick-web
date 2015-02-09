# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0015_tickethistory_update_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='fk_renter',
            new_name='fk_reporter',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fk_building',
            field=models.ForeignKey(to='ticketing.Building', blank=True, null=True, verbose_name='Building'),
            preserve_default=True,
        ),
    ]
