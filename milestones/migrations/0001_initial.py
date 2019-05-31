# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseContentMilestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('course_id', models.CharField(max_length=255, db_index=True)),
                ('content_id', models.CharField(max_length=255, db_index=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseMilestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('course_id', models.CharField(max_length=255, db_index=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('namespace', models.CharField(max_length=255, db_index=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('display_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneRelationshipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=25, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserMilestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('user_id', models.IntegerField(db_index=True)),
                ('source', models.TextField(blank=True)),
                ('collected', models.DateTimeField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('milestone', models.ForeignKey(to='milestones.Milestone')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='milestone',
            unique_together=set([('namespace', 'name')]),
        ),
        migrations.AddField(
            model_name='coursemilestone',
            name='milestone',
            field=models.ForeignKey(to='milestones.Milestone'),
        ),
        migrations.AddField(
            model_name='coursemilestone',
            name='milestone_relationship_type',
            field=models.ForeignKey(to='milestones.MilestoneRelationshipType'),
        ),
        migrations.AddField(
            model_name='coursecontentmilestone',
            name='milestone',
            field=models.ForeignKey(to='milestones.Milestone'),
        ),
        migrations.AddField(
            model_name='coursecontentmilestone',
            name='milestone_relationship_type',
            field=models.ForeignKey(to='milestones.MilestoneRelationshipType'),
        ),
        migrations.AlterUniqueTogether(
            name='usermilestone',
            unique_together=set([('user_id', 'milestone')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursemilestone',
            unique_together=set([('course_id', 'milestone')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursecontentmilestone',
            unique_together=set([('course_id', 'content_id', 'milestone')]),
        ),
    ]
