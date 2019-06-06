# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0003_coursecontentmilestone_requirements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecontentmilestone',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='coursemilestone',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='usermilestone',
            name='active',
            field=models.BooleanField(default=True, db_index=True),
        ),
    ]
