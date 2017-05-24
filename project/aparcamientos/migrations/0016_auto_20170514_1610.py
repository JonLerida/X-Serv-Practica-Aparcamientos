# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0015_estilo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estilo',
            name='color',
            field=models.CharField(max_length=20, default='black'),
        ),
        migrations.AlterField(
            model_name='estilo',
            name='size',
            field=models.IntegerField(default='1'),
        ),
    ]
