# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0009_company_fk_suitableeventcategories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='fk_suitableEventCategories',
            field=models.ManyToManyField(null=True, blank=True, to='ticketing.EventCategory'),
            preserve_default=True,
        ),
    ]
