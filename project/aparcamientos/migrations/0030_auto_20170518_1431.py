# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0029_aparcamiento_prueba'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aparcamiento',
            name='prueba',
        ),
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 18, 14, 31, 5, 917663, tzinfo=utc)),
        ),
    ]
