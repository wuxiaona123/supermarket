# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-22 18:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsClassModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('classname', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('classbrief', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsSKUModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goodsname', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('goodsbrief', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('sales', models.PositiveIntegerField()),
                ('head', models.ImageField(upload_to='goods/%y%m/%d', verbose_name='商品logo')),
                ('shelves', models.SmallIntegerField(choices=[(0, '未上架'), (1, '已上架')])),
                ('goodsclass_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsClassModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsSPUModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SPUname', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('SPUdetails', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='PhotoAlbumModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goodsImg', models.ImageField(upload_to='goods/%y%m/%d', verbose_name='商品相册')),
                ('goodsSKU', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKUModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('unitname', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='goodsskumodel',
            name='spu_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSPUModel'),
        ),
        migrations.AddField(
            model_name='goodsskumodel',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.UnitModel'),
        ),
    ]
