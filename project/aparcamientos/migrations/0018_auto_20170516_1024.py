# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0017_aparcamiento_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='codigo_postal',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='provincia',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='barrio',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='distrito',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.AlterField(
            model_name='pagina',
            name='nombre',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
