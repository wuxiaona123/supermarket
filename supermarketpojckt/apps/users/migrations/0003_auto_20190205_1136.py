# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-05 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190122_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodels',
            options={'verbose_name': '用户表', 'verbose_name_plural': '用户表'},
        ),
        migrations.AlterField(
            model_name='usermodels',
            name='head',
            field=models.ImageField(default='user/1901/21/favicon.png', upload_to='user/%y%m/%d', verbose_name='头像'),
        ),
    ]
