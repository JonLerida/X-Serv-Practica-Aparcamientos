# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0005_auto_20170513_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(to='aparcamientos.Usuario', null=True),
        ),
    ]
