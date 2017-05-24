# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0014_auto_20170513_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estilo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('size', models.IntegerField()),
                ('color', models.CharField(max_length=10)),
                ('usuario', models.ForeignKey(to='aparcamientos.Usuario')),
            ],
        ),
    ]
