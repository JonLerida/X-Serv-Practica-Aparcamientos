# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0007_comentario_aparcamiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(null=True, max_length=5),
        ),
    ]
