# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-21 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_auto_20170521_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tasklist',
            name='tags',
            field=models.ManyToManyField(blank=True, to='todolist.Tag'),
        ),
    ]
