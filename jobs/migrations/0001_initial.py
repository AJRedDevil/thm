# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Jobs'
        db.create_table(u'jobs_jobs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('fee', self.gf('django.db.models.fields.DecimalField')(max_digits=1000, decimal_places=2)),
            ('status', self.gf('django.db.models.fields.TextField')(default='New')),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('handymen', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('isaccepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isnotified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ishidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('distance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=1000, decimal_places=2)),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('available_handymen', self.gf('jsonfield.fields.JSONField')(default={})),
            ('tracking_number', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('considered_handymen', self.gf('django.db.models.fields.TextField')(default=[])),
        ))
        db.send_create_signal(u'jobs', ['Jobs'])


    def backwards(self, orm):
        # Deleting model 'Jobs'
        db.delete_table(u'jobs_jobs')


    models = {
        u'jobs.jobs': {
            'Meta': {'object_name': 'Jobs'},
            'available_handymen': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'considered_handymen': ('django.db.models.fields.TextField', [], {'default': '[]'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserProfile']"}),
            'distance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1000', 'decimal_places': '2'}),
            'fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '2'}),
            'handymen': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isaccepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isnotified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'New'"}),
            'tracking_number': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'blank': 'True'}),
            'address': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'displayname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '16'}),
            'phone_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        }
    }

    complete_apps = ['jobs']