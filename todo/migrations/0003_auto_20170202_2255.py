# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 22:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20170202_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='marked_complete_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marked_complete_by', to=settings.AUTH_USER_MODEL),
        ),
    ]