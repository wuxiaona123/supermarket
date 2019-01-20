# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-20 12:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.RegexValidator(message='手机号码格式不正确', regex='^1[34578]\\d{9}$')], verbose_name='手机号')),
                ('nickname', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='昵称')),
                ('password', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(32)], verbose_name='密码')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], verbose_name='性别')),
                ('school', models.CharField(max_length=50, verbose_name='学校')),
                ('hometown', models.CharField(max_length=100, verbose_name='老家')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
