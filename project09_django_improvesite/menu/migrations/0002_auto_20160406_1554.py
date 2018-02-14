# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('standard', models.BooleanField(default=False)),
                ('chef', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(to='menu.Ingredient')),
            ],
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='published_date',
            new_name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='chef',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='description',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title',
        ),
        migrations.AddField(
            model_name='menu',
            name='season',
            field=models.CharField(max_length=20, default=datetime.datetime(2016, 4, 6, 22, 54, 24, 258418, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(related_name='items', to='menu.Item'),
        ),
    ]
