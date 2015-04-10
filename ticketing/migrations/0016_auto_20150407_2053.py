# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0015_auto_20150407_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='fk_owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
