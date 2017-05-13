# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='aparcamientos',
            field=models.ManyToManyField(to='aparcamientos.Aparcamiento'),
        ),
    ]
