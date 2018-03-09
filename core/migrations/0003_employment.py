# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_account_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('currently_employed', models.BooleanField(default=False, verbose_name='Currently Employed')),
                ('wage', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Hourly Wage')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Account')),
            ],
        ),
    ]
