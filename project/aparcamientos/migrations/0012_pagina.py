# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0011_auto_20170513_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200, default=models.ForeignKey(to='aparcamientos.Usuario'))),
                ('enlace', models.CharField(max_length=200)),
                ('usuario', models.ForeignKey(to='aparcamientos.Usuario')),
            ],
        ),
    ]
