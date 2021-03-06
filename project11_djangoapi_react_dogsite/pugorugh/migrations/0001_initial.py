# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-09 08:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('image_filename', models.CharField(max_length=255)),
                ('breed', models.CharField(blank=True, max_length=255, verbose_name='Breed')),
                ('age', models.IntegerField(verbose_name='Age in month')),
                ('gender', models.CharField(blank=True, choices=[('m', 'male'), ('f', 'female')], max_length=1, verbose_name='Gender')),
                ('size', models.CharField(blank=True, choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'xlarge')], max_length=2, verbose_name='Size')),
                ('vaccinated', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'liked'), ('d', 'disliked'), ('u', 'undecided')], max_length=1, verbose_name='Status')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', multiselectfield.db.fields.MultiSelectField(choices=[('b', 'baby'), ('y', 'young'), ('a', 'adult'), ('s', 'senior')], default='b,y,a,s', max_length=50)),
                ('gender', multiselectfield.db.fields.MultiSelectField(choices=[('m', 'male'), ('f', 'female')], default='m,f', max_length=50)),
                ('size', multiselectfield.db.fields.MultiSelectField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'xlarge')], default='s,m,l,xl', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userdog',
            unique_together=set([('user', 'dog')]),
        ),
    ]
