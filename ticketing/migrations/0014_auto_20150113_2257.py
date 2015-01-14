# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0013_auto_20150110_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('language_name', models.CharField(max_length=50, default='English')),
                ('language_code', models.CharField(max_length=5, default='en-us')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='place',
            name='fk_building',
            field=models.ForeignKey(to='ticketing.Building'),
            preserve_default=True,
        ),
    ]
