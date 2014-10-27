# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(default='steve', unique=True, max_length=20),
            preserve_default=False,
        ),
    ]
