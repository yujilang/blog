# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_remove_comment_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p_comment', to='comment.Comment'),
        ),
    ]
