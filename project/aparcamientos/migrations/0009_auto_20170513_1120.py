# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0008_aparcamiento_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.CharField(max_length=1),
        ),
    ]
