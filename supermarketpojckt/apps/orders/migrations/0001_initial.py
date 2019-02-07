# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-05 11:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0006_auto_20190205_1136'),
        ('users', '0003_auto_20190205_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_sn', models.CharField(max_length=64, verbose_name='订单编号')),
                ('goods_total_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='商品总金额')),
                ('transport_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='运费')),
                ('transport', models.CharField(max_length=50, verbose_name='运输方式')),
                ('username', models.CharField(max_length=50, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='收货人电话号码')),
                ('address', models.CharField(max_length=250, verbose_name='收货人地址')),
                ('order_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='订单总金额')),
                ('order_status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付'), (2, '已发货'), (3, '未评价'), (4, '已完成'), (5, '退发货'), (6, '取消订单')], default=0, verbose_name='订单状态')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('deliver_time', models.DateTimeField(blank=True, null=True, verbose_name='发货时间')),
                ('finish_time', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
            ],
            options={
                'verbose_name': '订单管理',
                'verbose_name_plural': '订单管理',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='商品价格')),
                ('count', models.SmallIntegerField(verbose_name='订单商品数量')),
                ('goods_sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKUModel', verbose_name='订单商品ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order', verbose_name='订单ID')),
            ],
            options={
                'verbose_name': '订单商品管理',
                'verbose_name_plural': '订单商品管理',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='支付方式')),
                ('brief', models.CharField(max_length=200, verbose_name='说明')),
                ('logo', models.ImageField(upload_to='payment/%Y', verbose_name='支付LOGO')),
            ],
            options={
                'verbose_name': '支付方式管理',
                'verbose_name_plural': '支付方式管理',
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('up_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='运输方式')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='运费')),
            ],
            options={
                'verbose_name': '运输方式管理',
                'verbose_name_plural': '运输方式管理',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Payment', verbose_name='支付方式'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserModels', verbose_name='用户'),
        ),
    ]
