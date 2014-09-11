# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'Group name')),
                ('study', models.ForeignKey(to='studies.Study')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('stage_times_total', models.IntegerField(verbose_name=b'Total times for stage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='stages',
            field=models.ManyToManyField(to='studies.Stage', through='studies.GroupStage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupstage',
            name='group',
            field=models.ForeignKey(to='studies.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupstage',
            name='stage',
            field=models.ForeignKey(to='studies.Stage'),
            preserve_default=True,
        ),
    ]
