# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_ticketsuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsuser',
            name='first_name',
            field=models.CharField(max_length=30, default='', blank=True, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='ticketsuser',
            name='last_name',
            field=models.CharField(max_length=30, default='', blank=True, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='ticketsuser',
            name='phone_number',
            field=models.CharField(max_length=64, blank=True, null=True, verbose_name='Phone number'),
        ),
    ]
