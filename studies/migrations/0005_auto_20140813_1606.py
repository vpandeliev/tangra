# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0004_data_userstage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='group_stage',
        ),
        migrations.AddField(
            model_name='data',
            name='user_stage',
            field=models.ForeignKey(default=0, to='studies.UserStage'),
            preserve_default=False,
        ),
    ]
