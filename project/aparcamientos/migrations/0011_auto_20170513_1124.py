# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0010_auto_20170513_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(max_length=5),
        ),
    ]
