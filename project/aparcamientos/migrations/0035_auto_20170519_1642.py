# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0034_auto_20170519_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardado',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
