# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-21 23:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_auto_20170522_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('h', 'High'), ('m', 'Medium'), ('l', 'Low'), ('n', 'None')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='owner',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lists', to=settings.AUTH_USER_MODEL),
        ),
    ]