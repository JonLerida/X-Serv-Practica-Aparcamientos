# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0032_auto_20170518_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estilo',
            name='color',
            field=models.CharField(max_length=20, default='#D8FFD1'),
        ),
        migrations.AlterField(
            model_name='estilo',
            name='size',
            field=models.IntegerField(default='80'),
        ),
    ]
