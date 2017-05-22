# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0036_aparcamiento_puntuacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='puntuacion',
            field=models.IntegerField(blank=True, default='0'),
        ),
    ]
