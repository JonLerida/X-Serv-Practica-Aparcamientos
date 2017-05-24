# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0025_auto_20170517_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.BooleanField(default=False),
        ),
    ]
