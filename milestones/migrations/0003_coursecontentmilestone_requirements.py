# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0002_data__seed_relationship_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontentmilestone',
            name='requirements',
            field=models.CharField(help_text=b'Stores JSON data required to determine milestone fulfillment', max_length=255, null=True, blank=True),
        ),
    ]
