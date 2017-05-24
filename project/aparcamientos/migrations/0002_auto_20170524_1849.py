# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estilo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('size', models.IntegerField(default='80')),
                ('color', models.CharField(default='#D8FFD1', max_length=20)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guardado',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nombre', models.CharField(default='', max_length=200)),
                ('enlace', models.CharField(default='', max_length=200)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.RemoveField(
            model_name='aparcamiento',
            name='datos',
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='codigo_postal',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='email',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='localidad',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='number',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='provincia',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='puntuacion',
            field=models.IntegerField(blank=True, default='0'),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='telefono',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='via',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='comentario',
            name='aparcamiento',
            field=models.ForeignKey(null=True, to='aparcamientos.Aparcamiento'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='accesible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='barrio',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='distrito',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='latitud',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='nombre',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='guardado',
            name='aparcamiento',
            field=models.ForeignKey(to='aparcamientos.Aparcamiento'),
        ),
        migrations.AddField(
            model_name='guardado',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
