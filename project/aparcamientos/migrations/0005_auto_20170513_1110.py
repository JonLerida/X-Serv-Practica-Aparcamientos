# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0004_auto_20170513_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.IntegerField(max_length=1),
        ),
    ]
