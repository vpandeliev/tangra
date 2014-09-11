# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'Stage Name')),
                ('description', models.CharField(max_length=5000, verbose_name=b'Stage Description')),
                ('instructions', models.CharField(max_length=5000, verbose_name=b'Stage Instructions')),
                ('deadline', models.IntegerField(verbose_name=b'Time to finish session (in days)')),
                ('url', models.CharField(max_length=300, verbose_name=b'Stage URL')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'Study Name')),
                ('description', models.CharField(max_length=5000, verbose_name=b'Description')),
                ('consent', models.CharField(max_length=5000, verbose_name=b'Informed Consent Form')),
                ('instructions', models.CharField(max_length=5000, verbose_name=b'Study Instructions')),
                ('eligibility', models.CharField(max_length=5000, verbose_name=b'Eligibility Criteria')),
                ('reward', models.CharField(max_length=5000, verbose_name=b'Compensation and Reward')),
                ('start_date', models.DateField(null=True, verbose_name=b'Starting date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name=b'End date', blank=True)),
                ('started', models.BooleanField(default=False, verbose_name=b'Started')),
                ('investigators', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stage',
            name='study',
            field=models.ForeignKey(to='studies.Study'),
            preserve_default=True,
        ),
    ]
