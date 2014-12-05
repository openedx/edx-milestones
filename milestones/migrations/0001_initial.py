# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Milestone'
        db.create_table('milestones_milestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('namespace', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('milestones', ['Milestone'])

        # Adding model 'MilestoneRelationshipType'
        db.create_table('milestones_milestonerelationshiptype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('milestones', ['MilestoneRelationshipType'])

        # Adding model 'CourseMilestone'
        db.create_table('milestones_coursemilestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.Milestone'])),
            ('milestone_relationship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.MilestoneRelationshipType'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('milestones', ['CourseMilestone'])

        # Adding unique constraint on 'CourseMilestone', fields ['course_id', 'milestone']
        db.create_unique('milestones_coursemilestone', ['course_id', 'milestone_id'])

        # Adding model 'CourseContentMilestone'
        db.create_table('milestones_coursecontentmilestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('content_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.Milestone'])),
            ('milestone_relationship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.MilestoneRelationshipType'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('milestones', ['CourseContentMilestone'])

        # Adding unique constraint on 'CourseContentMilestone', fields ['course_id', 'content_id', 'milestone']
        db.create_unique('milestones_coursecontentmilestone', ['course_id', 'content_id', 'milestone_id'])

        # Adding model 'UserMilestone'
        db.create_table('milestones_usermilestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.Milestone'])),
            ('source', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('milestones', ['UserMilestone'])

        # Adding unique constraint on 'UserMilestone', fields ['user_id', 'milestone']
        db.create_unique('milestones_usermilestone', ['user_id', 'milestone_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserMilestone', fields ['user_id', 'milestone']
        db.delete_unique('milestones_usermilestone', ['user_id', 'milestone_id'])

        # Removing unique constraint on 'CourseContentMilestone', fields ['course_id', 'content_id', 'milestone']
        db.delete_unique('milestones_coursecontentmilestone', ['course_id', 'content_id', 'milestone_id'])

        # Removing unique constraint on 'CourseMilestone', fields ['course_id', 'milestone']
        db.delete_unique('milestones_coursemilestone', ['course_id', 'milestone_id'])

        # Deleting model 'Milestone'
        db.delete_table('milestones_milestone')

        # Deleting model 'MilestoneRelationshipType'
        db.delete_table('milestones_milestonerelationshiptype')

        # Deleting model 'CourseMilestone'
        db.delete_table('milestones_coursemilestone')

        # Deleting model 'CourseContentMilestone'
        db.delete_table('milestones_coursecontentmilestone')

        # Deleting model 'UserMilestone'
        db.delete_table('milestones_usermilestone')


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