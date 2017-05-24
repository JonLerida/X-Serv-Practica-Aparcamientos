# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0026_auto_20170517_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(default='', max_length=10),
        ),
    ]
