# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20150319_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='fk_renter',
            new_name='fk_owner',
        ),
    ]
