# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-10 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180310_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='share_key',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
