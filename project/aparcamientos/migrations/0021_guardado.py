# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0020_auto_20170516_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardado',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fecha', models.DateTimeField()),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
                ('usuario', models.ForeignKey(to='aparcamientos.Usuario')),
            ],
        ),
    ]
