# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-14 10:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20160314_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='previous_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_versions', to='subscriptions.Subscription'),
        ),
    ]
