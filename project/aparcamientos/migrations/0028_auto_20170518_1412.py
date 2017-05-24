# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0027_auto_20170518_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aparcamiento',
            old_name='datos',
            new_name='email',
        ),
        migrations.AddField(
            model_name='aparcamiento',
            name='telefono',
            field=models.CharField(blank=True, max_length=200, default=''),
        ),
    ]
