# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_watchedmovie_path'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Movies',
        ),
        migrations.RemoveField(
            model_name='accounts',
            name='id',
        ),
        migrations.AlterField(
            model_name='accounts',
            name='user_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
