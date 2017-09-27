# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170927_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounts',
            old_name='user_name',
            new_name='Name',
        ),
    ]
