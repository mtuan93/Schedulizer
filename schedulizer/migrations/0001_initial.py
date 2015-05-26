# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('subject_code', models.CharField(max_length=10)),
                ('course_number', models.CharField(max_length=4)),
                ('course_section', models.CharField(max_length=10)),
                ('course_title', models.CharField(max_length=50)),
                ('instructor', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('dates_given', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='course_ID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('term_name', models.CharField(max_length=10)),
                ('course_CRN', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='course',
            name='course_ID',
            field=models.ForeignKey(to='schedulizer.course_ID'),
            preserve_default=True,
        ),
    ]
