# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-22 23:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_activitymodel_rotationmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RotationModel',
            new_name='BannerModel',
        ),
        migrations.AlterModelTable(
            name='bannermodel',
            table='BannerModel',
        ),
    ]
