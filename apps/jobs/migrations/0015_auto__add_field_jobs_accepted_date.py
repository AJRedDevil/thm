# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Jobs.accepted_date'
        db.add_column(u'jobs_jobs', 'accepted_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Jobs.accepted_date'
        db.delete_column(u'jobs_jobs', 'accepted_date')


    models = {
        u'jobs.jobevents': {
            'Meta': {'object_name': 'JobEvents'},
            'event': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Jobs']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'jobs.jobs': {
            'Meta': {'object_name': 'Jobs'},
            'accepted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'available_handymen': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'considered_handymen': ('django.db.models.fields.TextField', [], {'default': '[]'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': u"orm['users.UserProfile']"}),
            'destination_home': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1000', 'decimal_places': '2'}),
            'fee': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'NPR'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'fee_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"}),
            'handyman': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orders'", 'symmetrical': 'False', 'to': u"orm['users.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jobref': ('django.db.models.fields.CharField', [], {'default': "'f4abceff078949f5a5077591080a1756'", 'unique': 'True', 'max_length': '100'}),
            'jobtype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'remarks': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'address': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'current_address': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '16'}),
            'phone_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'userref': ('django.db.models.fields.CharField', [], {'default': "'a20af52be65d41f08f709727948e9b56'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['jobs']