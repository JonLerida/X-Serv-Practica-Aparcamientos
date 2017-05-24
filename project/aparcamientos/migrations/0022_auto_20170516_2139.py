# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0021_guardado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.CharField(default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='datos',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='latitud',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='nombre',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nick',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
