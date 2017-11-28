# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_auto_20171107_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(default=160),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Video'),
        ),
    ]
