# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0020_auto_20150416_1557'),
        ('login', '0007_ticketsuser_fk_entreprise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketsuser',
            name='fk_entreprise',
        ),
        migrations.AddField(
            model_name='ticketsuser',
            name='fk_company',
            field=models.ForeignKey(blank=True, verbose_name='Linked company', null=True, default=None, to='ticketing.Company'),
        ),
    ]
