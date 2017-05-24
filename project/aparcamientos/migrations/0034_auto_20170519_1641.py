# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0033_auto_20170519_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='aparcamientos',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
