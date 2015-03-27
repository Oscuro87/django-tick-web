# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150109_2348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='date_joined',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='first_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='is_active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='is_staff',
            new_name='is_staff',
        ),
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='last_name',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='ticketsuser',
            old_name='receive_newsletter',
            new_name='receive_newsletter',
        ),
    ]
