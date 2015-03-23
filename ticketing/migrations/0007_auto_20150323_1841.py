# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0006_auto_20150319_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='building_code',
            field=models.CharField(max_length=10, unique=True, default='', verbose_name='Building code'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_company',
            field=models.ForeignKey(null=True, blank=True, to='ticketing.Company'),
            preserve_default=True,
        ),
    ]
