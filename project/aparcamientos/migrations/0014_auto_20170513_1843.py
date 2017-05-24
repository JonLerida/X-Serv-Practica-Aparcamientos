# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0013_auto_20170513_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagina',
            name='enlace',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='pagina',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
