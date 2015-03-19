# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=45, verbose_name='Street', unique=True)),
                ('vicinity', models.CharField(max_length=45, verbose_name='Vicinity name', default='')),
                ('postcode', models.IntegerField(verbose_name='Postcode', default='0')),
                ('building_name', models.CharField(max_length=45, verbose_name='Building name', default='', unique=True)),
                ('building_code', models.CharField(max_length=4, verbose_name='Building code', default='', unique=True)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
            ],
            options={
                'verbose_name_plural': 'Buildings',
                'ordering': ['building_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=64, verbose_name='Way of ticket creation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=45, verbose_name='Street', unique=True)),
                ('vicinity', models.CharField(max_length=45, verbose_name='Vicinity name', default='')),
                ('postcode', models.IntegerField(verbose_name='Postcode', default='0')),
                ('phone_number', models.CharField(max_length=45, null=True, verbose_name='Telephone number', default='', blank=True)),
                ('name', models.CharField(max_length=45, verbose_name='Company name')),
                ('vat_number', models.CharField(max_length=45, verbose_name='VAT Number', unique=True)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=45, verbose_name='Incident label')),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('fk_company', models.ForeignKey(unique=True, to='ticketing.Company')),
                ('fk_parent_category', models.ForeignKey(default=None, null=True, blank=True, to='ticketing.EventCategory')),
            ],
            options={
                'verbose_name_plural': 'Event categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('fk_building', models.ForeignKey(to='ticketing.Building')),
                ('fk_renter', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('ticket_code', models.CharField(max_length=10, verbose_name='Ticket code', blank=True, unique=True)),
                ('floor', models.CharField(max_length=45, null=True, default='', blank=True)),
                ('office', models.CharField(max_length=45, null=True, default='', blank=True)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('intervention_date', models.DateField(null=True, verbose_name='Date of intervention', default=None, blank=True)),
                ('description', models.TextField(null=True, verbose_name='Event description', default='No description available.', blank=True)),
                ('fk_building', models.ForeignKey(verbose_name='Building', null=True, blank=True, to='ticketing.Building')),
                ('fk_category', models.ForeignKey(verbose_name='Category', to='ticketing.EventCategory')),
                ('fk_channel', models.ForeignKey(verbose_name='Channel', to='ticketing.Channel')),
                ('fk_company', models.ForeignKey(verbose_name='Company', null=True, blank=True, to='ticketing.Company')),
                ('fk_manager', models.ForeignKey(verbose_name='Manager', null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='gestionnaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(verbose_name='Comment date', auto_now_add=True, null=True)),
                ('comment', models.TextField(verbose_name='Comment', default='No comment provided.')),
                ('fk_commenter', models.ForeignKey(verbose_name='Commenter', default=None, to=settings.AUTH_USER_MODEL)),
                ('fk_ticket', models.ForeignKey(verbose_name='Ticket', default=None, to='ticketing.Ticket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('update_date', models.DateTimeField(verbose_name='Updated on...', auto_now_add=True)),
                ('update_reason', models.CharField(max_length=200, verbose_name='Update reason', default='No reason given.', blank=True)),
                ('fk_manager', models.ForeignKey(verbose_name='Who changed the status', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('fk_ticket', models.ForeignKey(to='ticketing.Ticket')),
            ],
            options={
                'verbose_name_plural': 'Ticket histories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=64, verbose_name='Priority')),
            ],
            options={
                'verbose_name_plural': 'Ticket priorities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=64, verbose_name='Status')),
            ],
            options={
                'verbose_name_plural': 'Ticket statuses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='fk_ticket_status',
            field=models.ForeignKey(to='ticketing.TicketStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_priority',
            field=models.ForeignKey(verbose_name='Priority', to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_reporter',
            field=models.ForeignKey(verbose_name='Reporter', related_name='rapporteur', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_status',
            field=models.ForeignKey(verbose_name='Status', default=1, to='ticketing.TicketStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='fk_priority',
            field=models.ForeignKey(to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
    ]
