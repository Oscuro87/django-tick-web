# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0008_remove_eventcategory_fk_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='fk_suitableEventCategories',
            field=models.ManyToManyField(to='ticketing.EventCategory'),
            preserve_default=True,
        ),
    ]
