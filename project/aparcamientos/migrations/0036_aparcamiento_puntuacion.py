# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0035_auto_20170519_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='puntuacion',
            field=models.CharField(blank=True, default='0', max_length=3),
        ),
    ]
