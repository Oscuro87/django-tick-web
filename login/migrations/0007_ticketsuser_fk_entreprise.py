# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0020_auto_20150416_1557'),
        ('login', '0006_auto_20150416_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsuser',
            name='fk_entreprise',
            field=models.ForeignKey(blank=True, null=True, default=None, to='ticketing.Company'),
        ),
    ]
