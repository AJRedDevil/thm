# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfile.first_name'
        db.delete_column(u'users_userprofile', 'first_name')

        # Deleting field 'UserProfile.last_name'
        db.delete_column(u'users_userprofile', 'last_name')

        # Deleting field 'UserProfile.displayname'
        db.delete_column(u'users_userprofile', 'displayname')

        # Deleting field 'UserProfile.email'
        db.delete_column(u'users_userprofile', 'email')

        # Adding field 'UserProfile.name'
        db.add_column(u'users_userprofile', 'name',
                      self.gf('django.db.models.fields.CharField')(default='HM', max_length=30),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'UserProfile.first_name'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.first_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserProfile.first_name'
        db.add_column(u'users_userprofile', 'first_name',
                      self.gf('django.db.models.fields.CharField')(max_length=30),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserProfile.last_name'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.last_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserProfile.last_name'
        db.add_column(u'users_userprofile', 'last_name',
                      self.gf('django.db.models.fields.CharField')(max_length=30),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserProfile.displayname'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.displayname' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserProfile.displayname'
        db.add_column(u'users_userprofile', 'displayname',
                      self.gf('django.db.models.fields.CharField')(max_length=30, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserProfile.email'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.email' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserProfile.email'
        db.add_column(u'users_userprofile', 'email',
                      self.gf('django.db.models.fields.EmailField')(max_length=100),
                      keep_default=False)

        # Deleting field 'UserProfile.name'
        db.delete_column(u'users_userprofile', 'name')


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
        }
    }

    complete_apps = ['users']