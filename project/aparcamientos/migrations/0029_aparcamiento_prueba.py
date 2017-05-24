# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0028_auto_20170518_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='prueba',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
