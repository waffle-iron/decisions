# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-14 09:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0003_auto_20160306_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionhit',
            options={'get_latest_by': 'created', 'verbose_name': 'subscription hit', 'verbose_name_plural': 'subscription hits'},
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.RemoveField(
            model_name='subscriptionhit',
            name='subscription',
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscriptionhit',
            name='subscriptions',
            field=models.ManyToManyField(to='subscriptions.Subscription'),
        ),
    ]
