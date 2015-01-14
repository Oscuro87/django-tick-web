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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('address', models.CharField(verbose_name='Street', unique=True, max_length=45)),
                ('vicinity', models.CharField(verbose_name='Vicinity name', max_length=45, default='')),
                ('postcode', models.IntegerField(verbose_name='Postcode', default='0')),
                ('building_name', models.CharField(verbose_name='Building name', unique=True, max_length=45, default='')),
                ('building_code', models.CharField(verbose_name='Building code', unique=True, max_length=4, default='')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Way of ticket creation', max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('address', models.CharField(verbose_name='Street', unique=True, max_length=45)),
                ('vicinity', models.CharField(verbose_name='Vicinity name', max_length=45, default='')),
                ('postcode', models.IntegerField(verbose_name='Postcode', default='0')),
                ('phone_number', models.CharField(verbose_name='Telephone number', null=True, max_length=45, blank=True, default='')),
                ('name', models.CharField(verbose_name='Company name', max_length=45)),
                ('vat_number', models.CharField(verbose_name='VAT Number', unique=True, max_length=45)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Incident label', max_length=45)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('fk_company', models.OneToOneField(null=True, to='ticketing.Company', default=None)),
                ('fk_parent_category', models.OneToOneField(null=True, to='ticketing.EventCategory', default=None)),
            ],
            options={
                'verbose_name_plural': 'Event categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('fk_building', models.OneToOneField(to='ticketing.Building')),
                ('fk_renter', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.TextField(verbose_name='Event description', null=True, blank=True, default='No description available.')),
                ('intervention_date', models.DateField(verbose_name='Date of intervention', null=True, blank=True, default=None)),
                ('ticket_code', models.CharField(verbose_name='Ticket code', unique=True, max_length=10)),
                ('floor', models.CharField(null=True, max_length=45, blank=True, default='')),
                ('office', models.CharField(null=True, max_length=45, blank=True, default='')),
                ('visible', models.BooleanField(verbose_name='Is visible?', default=True)),
                ('fk_building', models.OneToOneField(to='ticketing.Building')),
                ('fk_category', models.OneToOneField(to='ticketing.EventCategory')),
                ('fk_channel', models.OneToOneField(to='ticketing.Channel')),
                ('fk_company', models.OneToOneField(null=True, to='ticketing.Company', blank=True)),
                ('fk_manager', models.OneToOneField(null=True, related_name='gestionnaire', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('update_date', models.DateTimeField(verbose_name='Updated on...', auto_now_add=True)),
                ('fk_manager', models.OneToOneField(verbose_name='Who changed the status', to=settings.AUTH_USER_MODEL)),
                ('fk_ticket', models.OneToOneField(to='ticketing.Ticket')),
            ],
            options={
                'verbose_name_plural': 'Ticket histories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Priority', max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Ticket priorities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Status', max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Ticket statuses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='fk_ticket_status',
            field=models.OneToOneField(to='ticketing.TicketStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_priority',
            field=models.OneToOneField(to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_renter',
            field=models.OneToOneField(related_name='locataire', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='fk_status',
            field=models.OneToOneField(to='ticketing.TicketStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='fk_priority',
            field=models.OneToOneField(to='ticketing.TicketPriority'),
            preserve_default=True,
        ),
    ]
