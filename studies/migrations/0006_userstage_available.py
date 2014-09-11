# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0005_auto_20140813_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstage',
            name='available',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
