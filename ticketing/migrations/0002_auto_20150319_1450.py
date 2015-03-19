# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcategory',
            name='fk_company',
            field=models.ForeignKey(to='ticketing.Company', unique=True, null=True),
            preserve_default=True,
        ),
    ]
