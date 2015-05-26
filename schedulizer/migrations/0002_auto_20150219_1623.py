# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedulizer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_ID',
        ),
        migrations.DeleteModel(
            name='course_ID',
        ),
        migrations.AddField(
            model_name='course',
            name='course_CRN',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='term_name',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='end_time',
            field=models.TimeField(verbose_name='End Time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='start_time',
            field=models.TimeField(verbose_name='Start Time'),
            preserve_default=True,
        ),
    ]
