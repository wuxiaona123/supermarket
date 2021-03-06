# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-22 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20190122_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('activityName', models.CharField(max_length=30)),
                ('imgUrl', models.ImageField(upload_to='activity/%y%m/%d', verbose_name='活动图片')),
                ('urlUrl', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '首页活动表',
                'verbose_name_plural': '首页活动表',
                'db_table': 'ActivityModel',
            },
        ),
        migrations.CreateModel(
            name='RotationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('bannerName', models.CharField(max_length=30)),
                ('goodsImg', models.ImageField(upload_to='banner/%y%m/%d', verbose_name='商品相册')),
                ('bannerOrder', models.SmallIntegerField()),
                ('goodsSKU', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKUModel', verbose_name='商品SKU')),
            ],
            options={
                'verbose_name': '首页轮播商品表',
                'verbose_name_plural': '首页轮播商品表',
                'db_table': 'RotationModel',
            },
        ),
    ]
