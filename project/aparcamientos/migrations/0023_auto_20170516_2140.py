# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0022_auto_20170516_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='barrio',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='codigo_postal',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='datos',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='distrito',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='provincia',
            field=models.CharField(max_length=30, blank=True, default=''),
        ),
    ]
