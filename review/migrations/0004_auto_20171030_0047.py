# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='vote_count',
        ),
        migrations.AddField(
            model_name='movies',
            name='backdrop',
            field=models.URLField(blank=True, null=True, verbose_name='Background'),
        ),
    ]
