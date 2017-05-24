# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0012_pagina'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagina',
            name='nombre',
            field=models.CharField(max_length=200, default='Pagina de '),
        ),
    ]
