# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email address', default='', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsuser',
            name='firstName',
            field=models.CharField(max_length=30, verbose_name='first name', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsuser',
            name='isActive',
            field=models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsuser',
            name='lastName',
            field=models.CharField(max_length=30, verbose_name='last name', default=''),
            preserve_default=True,
        ),
    ]
