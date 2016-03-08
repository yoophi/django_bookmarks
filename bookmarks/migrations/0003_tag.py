# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_bookmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('bookmarks', models.ManyToManyField(to='bookmarks.Bookmark')),
            ],
        ),
    ]
