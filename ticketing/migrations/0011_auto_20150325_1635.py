# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0010_auto_20150325_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='fk_suitableEventCategories',
            field=models.ManyToManyField(blank=True, to='ticketing.EventCategory', verbose_name='Suitable Event Categories', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='vat_number',
            field=models.CharField(unique=True, blank=True, verbose_name='VAT Number', max_length=45, null=True),
            preserve_default=True,
        ),
    ]
