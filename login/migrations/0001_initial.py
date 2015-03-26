# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('firstName', models.CharField(default='NOT SET!', max_length=30, verbose_name='first name')),
                ('lastName', models.CharField(default='NOT SET!', max_length=30, verbose_name='last name')),
                ('email', models.EmailField(default='NOT SET!', max_length=255, unique=True, verbose_name='email address')),
                ('isStaff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('isActive', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('dateJoined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('receiveNewsletter', models.BooleanField(default=False, verbose_name='receive newsletter')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', related_query_name='user', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', help_text='Specific permissions for this user.', to='auth.Permission', related_query_name='user', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
