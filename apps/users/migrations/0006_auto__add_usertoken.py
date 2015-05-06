# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserToken'
        db.create_table(u'users_usertoken', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('token', self.gf('django.db.models.fields.CharField')(default='23bbfc0b74d121210813', max_length=20, primary_key=True)),
            ('timeframe', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 24, 0, 0))),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['UserToken'])


    def backwards(self, orm):
        # Deleting model 'UserToken'
        db.delete_table(u'users_usertoken')


    models = {
        u'users.earlybirdhandymen': {
            'Meta': {'object_name': 'EarlyBirdHandymen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '16'}),
            'registered_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'users.earlybirduser': {
            'Meta': {'object_name': 'EarlyBirdUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '16'}),
            'registered_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'users.userevents': {
            'Meta': {'object_name': 'UserEvents'},
            'event': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserProfile']"})
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
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'users.usertoken': {
            'Meta': {'object_name': 'UserToken'},
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timeframe': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 24, 0, 0)'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'23bbfc0b74d121210813'", 'max_length': '20', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserProfile']"})
        }
    }

    complete_apps = ['users']