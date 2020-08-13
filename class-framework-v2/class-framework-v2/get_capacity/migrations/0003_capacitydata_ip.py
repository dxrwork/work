# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_capacity', '0002_capacitydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='capacitydata',
            name='ip',
            field=models.CharField(max_length=64, null=True, verbose_name=b'ip', blank=True),
        ),
    ]
