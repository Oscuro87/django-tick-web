# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_auto_20150107_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_parent_category',
            field=models.ForeignKey(blank=True, null=True, default=None, to='ticketing.EventCategory'),
            preserve_default=True,
        ),
    ]
