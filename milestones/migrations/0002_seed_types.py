# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.MilestoneRelationshipType.objects.create(
            name='requires',
            description='Establishes a dependency between an entity and the milestone',
            active=True
        )
        orm.MilestoneRelationshipType.objects.create(
            name='fulfills',
            description='Specifies an entity as a producer of a milestone',
            active=True
        )
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        # If we're running this backwards migration we must be rolling back beyond the
        # seed procedure to initial/clean state.  So, remove all Milestone Relationship Types
        orm.MilestoneRelationshipType.objects.all().delete()

    models = {
        'milestones.coursecontentmilestone': {
            'Meta': {'unique_together': "(('course_id', 'content_id', 'milestone'),)", 'object_name': 'CourseContentMilestone'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.Milestone']"}),
            'milestone_relationship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.MilestoneRelationshipType']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        'milestones.coursemilestone': {
            'Meta': {'unique_together': "(('course_id', 'milestone'),)", 'object_name': 'CourseMilestone'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.Milestone']"}),
            'milestone_relationship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.MilestoneRelationshipType']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        'milestones.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'milestones.milestonerelationshiptype': {
            'Meta': {'object_name': 'MilestoneRelationshipType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'milestones.usermilestone': {
            'Meta': {'unique_together': "(('user_id', 'milestone'),)", 'object_name': 'UserMilestone'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.Milestone']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'source': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['milestones']
    symmetrical = True
