# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0006_comentario_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='aparcamiento',
            field=models.ForeignKey(to='aparcamientos.Aparcamiento', null=True),
        ),
    ]
