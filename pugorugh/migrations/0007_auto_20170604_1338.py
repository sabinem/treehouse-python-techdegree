# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-04 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import pugorugh.models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0006_auto_20170604_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(max_length=2, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(max_length=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(default='b,y,a,s', max_length=50, verbose_name='Age Preference List'),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(default='f,m', max_length=50, verbose_name='Gender Preference List'),
        ),
    ]
