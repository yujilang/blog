# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171019_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar/1.jpg', upload_to='avatar/'),
        ),
    ]
