# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0013_auto_20150330_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='fk_suitableEventCategories',
            field=models.ManyToManyField(blank=True, to='ticketing.EventCategory', verbose_name='Suitable Event Categories'),
        ),
        migrations.AlterField(
            model_name='company',
            name='vat_number',
            field=models.CharField(blank=True, max_length=45, verbose_name='VAT Number', null=True),
        ),
    ]
