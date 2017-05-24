# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0016_auto_20170514_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
