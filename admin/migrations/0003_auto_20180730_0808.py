# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-30 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_goodsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsClassifyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_classify', models.CharField(max_length=20, verbose_name='商品分类')),
            ],
            options={
                'db_table': 'tb_goods_classsify',
            },
        ),
        migrations.AlterField(
            model_name='goodsmodel',
            name='goods_classify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='admin.GoodsClassifyModel', verbose_name='商品分类'),
        ),
        migrations.AlterModelTable(
            name='goodsmodel',
            table='tb_goods',
        ),
    ]
