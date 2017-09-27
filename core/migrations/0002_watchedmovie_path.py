# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchedmovie',
            name='path',
            field=models.CharField(default='/2Sns5oMb356JNdBHgBETjIpRYy9.jpg', max_length=25),
            preserve_default=False,
        ),
    ]
