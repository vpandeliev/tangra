# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0002_auto_20140807_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupstage',
            name='stage_times_total',
        ),
    ]
