# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0010_auto_20170321_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='total_price',
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Сумма'),
        ),
        migrations.AddField(
            model_name='reservationorder',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Общая сумма'),
        ),
    ]
