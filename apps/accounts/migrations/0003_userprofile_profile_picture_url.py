# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-04 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171130_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]