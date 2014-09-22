# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0006_userstage_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name=b'users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='study',
            name='investigators',
            field=models.ManyToManyField(related_name=b'investigators', to=settings.AUTH_USER_MODEL),
        ),
    ]
