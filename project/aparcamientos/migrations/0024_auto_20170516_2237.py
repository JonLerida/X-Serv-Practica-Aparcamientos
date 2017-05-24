# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0023_auto_20170516_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='localidad',
            field=models.CharField(max_length=100, default='', blank=True),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='via',
            field=models.CharField(max_length=100, default='', blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.CharField(max_length=1, default='', blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='descripcion',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='url',
            field=models.CharField(max_length=200, default='', blank=True),
        ),
    ]
