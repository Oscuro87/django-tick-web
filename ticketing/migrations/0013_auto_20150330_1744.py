# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0012_auto_20150325_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='postcode',
            field=models.CharField(verbose_name='Postcode', default='', max_length=10),
            preserve_default=True,
        ),
    ]
