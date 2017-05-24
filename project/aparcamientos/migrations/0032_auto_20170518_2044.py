# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0031_auto_20170518_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='nombre',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(blank=True, max_length=10, default=''),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(default=''),
        ),
    ]
