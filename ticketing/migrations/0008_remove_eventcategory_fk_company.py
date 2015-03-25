# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0007_auto_20150323_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventcategory',
            name='fk_company',
        ),
    ]
