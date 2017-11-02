# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_auto_20171102_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castandcrew',
            name='biography',
            field=models.TextField(blank=True, default='Biography yet to added', null=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='castandcrew',
            name='birthday',
            field=models.DateField(blank=True, default='2017-08-11', null=True),
        ),
        migrations.AlterField(
            model_name='castandcrew',
            name='popularity',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
